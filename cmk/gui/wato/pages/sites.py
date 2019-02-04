#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2014             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.
"""Mode for managing sites"""

import traceback
import time
import multiprocessing
import Queue
from typing import TypeVar, List, Dict, NamedTuple  # pylint: disable=unused-import

import cmk
import cmk.gui.config as config
import cmk.gui.watolib as watolib
import cmk.gui.forms as forms
import cmk.gui.log as log
from cmk.gui.table import table_element
from cmk.gui.valuespec import (
    Dictionary,
    ID,
    Integer,
    FixedValue,
    TextUnicode,
    TextAscii,
    Checkbox,
    Tuple,
    Alternative,
    DropdownChoice,
    MonitoredHostname,
    HTTPUrl,
)

from cmk.gui.plugins.wato.utils import mode_registry, sort_sites
from cmk.gui.plugins.wato.utils.base_modes import WatoMode, WatoWebApiMode
from cmk.gui.plugins.wato.utils.html_elements import wato_html_head, wato_confirm
from cmk.gui.i18n import _
from cmk.gui.globals import html
from cmk.gui.exceptions import MKUserError
from cmk.gui.log import logger

from cmk.gui.watolib.activate_changes import clear_site_replication_status
from cmk.gui.wato.pages.global_settings import GlobalSettingsMode, is_a_checkbox


@mode_registry.register
class ModeEditSite(WatoMode):
    @classmethod
    def name(cls):
        return "edit_site"

    @classmethod
    def permissions(cls):
        return ["sites"]

    def __init__(self):
        super(ModeEditSite, self).__init__()
        self._site_mgmt = watolib.SiteManagementFactory().factory()

        self._site_id = html.request.var("edit")
        self._clone_id = html.request.var("clone")
        self._new = self._site_id is None

        configured_sites = self._site_mgmt.load_sites()

        if self._clone_id:
            try:
                self._site = configured_sites[self._clone_id]
            except KeyError:
                raise MKUserError(None, _("The requested site does not exist"))

        elif self._new:
            self._site = {
                "replicate_mkps": True,
                "replicate_ec": True,
                "socket": ("tcp", {
                    "address": ("", 6557),
                    "tls": ("encrypted", {
                        "verify": True,
                    })
                }),
                "timeout": 5,
                "disable_wato": True,
                "user_login": True,
                "replication": None,
            }

        else:
            try:
                self._site = configured_sites[self._site_id]
            except KeyError:
                raise MKUserError(None, _("The requested site does not exist"))

    def title(self):
        if self._new:
            return _("Create new site connection")
        return _("Edit site connection %s") % self._site_id

    def buttons(self):
        super(ModeEditSite, self).buttons()
        html.context_button(
            _("All Sites"), watolib.folder_preserving_link([("mode", "sites")]), "back")
        if not self._new and self._site["replication"]:
            html.context_button(
                _("Site-Globals"),
                watolib.folder_preserving_link([("mode", "edit_site_globals"),
                                                ("site", self._site_id)]), "configuration")

    def action(self):
        if not html.check_transaction():
            return "sites"

        vs = self._valuespec()
        site_spec = vs.from_html_vars("site")
        vs.validate_value(site_spec, "site")

        # Extract the ID. It is not persisted in the site value
        if self._new:
            self._site_id = site_spec["id"]
        del site_spec["id"]

        configured_sites = self._site_mgmt.load_sites()

        # Take over all unknown elements from existing site specs, like for
        # example, the replication secret
        for key, value in configured_sites.get(self._site_id, {}).items():
            site_spec.setdefault(key, value)

        self._site_mgmt.validate_configuration(self._site_id, site_spec, configured_sites)

        self._site = configured_sites[self._site_id] = site_spec
        self._site_mgmt.save_sites(configured_sites)

        if self._new:
            msg = _("Created new connection to site %s") % html.render_tt(self._site_id)
        else:
            msg = _("Modified site connection %s") % html.render_tt(self._site_id)

        # Don't know exactly what have been changed, so better issue a change
        # affecting all domains
        watolib.add_change(
            "edit-sites",
            msg,
            sites=[self._site_id],
            domains=watolib.ConfigDomain.enabled_domains())

        # In case a site is not being replicated anymore, confirm all changes for this site!
        if not site_spec["replication"]:
            clear_site_replication_status(self._site_id)

        if self._site_id != config.omd_site():
            # On central site issue a change only affecting the GUI
            watolib.add_change(
                "edit-sites", msg, sites=[config.omd_site()], domains=[watolib.ConfigDomainGUI])

        return "sites", msg

    def page(self):
        html.begin_form("site")

        self._valuespec().render_input("site", self._site)

        forms.end()
        html.button("save", _("Save"))
        html.hidden_fields()
        html.end_form()

    def _valuespec(self):
        basic_elements = self._basic_elements()
        livestatus_elements = self._livestatus_elements()
        replication_elements = self._replication_elements()

        return Dictionary(
            elements=basic_elements + livestatus_elements + replication_elements,
            headers=[
                (_("Basic settings"), [key for key, _vs in basic_elements]),
                (_("Livestatus settings"), [key for key, _vs in livestatus_elements]),
                (_("Configuration Replication"), [key for key, _vs in replication_elements]),
            ],
            render="form",
            form_narrow=True,
            optional_keys=[],
        )

    def _basic_elements(self):
        if self._new:
            vs_site_id = ID(
                title=_("Site ID"),
                size=60,
                allow_empty=False,
                help=_("The site ID must be identical (case sensitive) with "
                       "the instance's exact name."),
                validate=self._validate_site_id,
            )
        else:
            vs_site_id = FixedValue(
                self._site_id,
                title=_("Site ID"),
            )

        return [
            ("id", vs_site_id),
            ("alias",
             TextUnicode(
                 title=_("Alias"),
                 size=60,
                 help=_("An alias or description of the site."),
                 allow_empty=False,
             )),
        ]

    def _validate_site_id(self, value, varprefix):
        if value in self._site_mgmt.load_sites():
            raise MKUserError("id", _("This id is already being used by another connection."))

    def _livestatus_elements(self):
        proxy_docu_url = "https://mathias-kettner.com/checkmk_multisite_modproxy.html"
        status_host_docu_url = "https://mathias-kettner.com/checkmk_multisite_statushost.html"
        site_choices = [("", _("(no status host)"))] + [
            (sk, si.get("alias", sk)) for (sk, si) in self._site_mgmt.load_sites().items()
        ]

        return [
            ("socket", self._site_mgmt.connection_method_valuespec()),
            ("proxy", self._site_mgmt.livestatus_proxy_valuespec()),
            ("timeout",
             Integer(
                 title=_("Connect timeout"),
                 size=2,
                 unit=_("Seconds"),
                 minvalue=0,
                 help=_("This sets the time that Multisite waits for a connection "
                        "to the site to be established before the site is "
                        "considered to be unreachable. If not set, the operating system "
                        "defaults are begin used and just one login attempt is being. "
                        "performed."),
             )),
            ("persist",
             Checkbox(
                 title=_("Persistent Connection"),
                 label=_("Use persistent connections"),
                 help=
                 _("If you enable persistent connections then Multisite will try to keep open "
                   "the connection to the remote sites. This brings a great speed up in high-latency "
                   "situations but locks a number of threads in the Livestatus module of the target site."
                  ),
             )),
            ("url_prefix",
             TextAscii(
                 title=_("URL prefix"),
                 size=60,
                 help=
                 _("The URL prefix will be prepended to links of addons like PNP4Nagios "
                   "or the classical Nagios GUI when a link to such applications points to a host or "
                   "service on that site. You can either use an absolute URL prefix like <tt>http://some.host/mysite/</tt> "
                   "or a relative URL like <tt>/mysite/</tt>. When using relative prefixes you needed a mod_proxy "
                   "configuration in your local system apache that proxies such URLs to the according remote site. "
                   "Please refer to the <a target=_blank href='%s'>online documentation</a> for details. "
                   "The prefix should end with a slash. Omit the <tt>/pnp4nagios/</tt> from the prefix."
                  ) % proxy_docu_url,
                 allow_empty=False,
             )),
            ("status_host",
             Alternative(
                 title=_("Status host"),
                 style="dropdown",
                 elements=[
                     FixedValue(None, title=_("No status host"), totext=""),
                     Tuple(
                         title=_("Use the following status host"),
                         orientation="horizontal",
                         elements=[
                             DropdownChoice(
                                 title=_("Site:"),
                                 choices=site_choices,
                                 sorted=True,
                             ),
                             self._vs_host(),
                         ],
                     ),
                 ],
                 help=
                 _("By specifying a status host for each non-local connection "
                   "you prevent Multisite from running into timeouts when remote sites do not respond. "
                   "You need to add the remote monitoring servers as hosts into your local monitoring "
                   "site and use their host state as a reachability state of the remote site. Please "
                   "refer to the <a target=_blank href='%s'>online documentation</a> for details.")
                 % status_host_docu_url,
             )),
            ("disabled",
             Checkbox(
                 title=_("Disable in status GUI"),
                 label=_("Temporarily disable this connection"),
                 help=_(
                     "If you disable a connection, then no data of this site will be shown in the status GUI. "
                     "The replication is not affected by this, however."),
             )),
        ]

    def _vs_host(self):
        return MonitoredHostname(
            title=_("Host:"),
            allow_empty=False,
        )

    def _replication_elements(self):
        return [
            ("replication",
             DropdownChoice(
                 title=_("Enable replication"),
                 choices=[
                     (None, _("No replication with this site")),
                     ("slave", _("Push configuration to this site")),
                 ],
                 help=_("WATO replication allows you to manage several monitoring sites with a "
                        "logically centralized WATO. Remote sites receive their configuration "
                        "from the central sites. <br><br>Note: Remote sites "
                        "do not need any replication configuration. They will be remote-controlled "
                        "by the central sites."),
             )),
            ("multisiteurl",
             HTTPUrl(
                 title=_("URL of remote site"),
                 size=60,
                 help=_(
                     "URL of the remote Check_MK including <tt>/check_mk/</tt>. "
                     "This URL is in many cases the same as the URL-Prefix but with <tt>check_mk/</tt> "
                     "appended, but it must always be an absolute URL. Please note, that "
                     "that URL will be fetched by the Apache server of the local "
                     "site itself, whilst the URL-Prefix is used by your local Browser."),
                 allow_empty=True,
             )),
            ("disable_wato",
             Checkbox(
                 title=_("Disable remote configuration"),
                 label=_('Disable configuration via WATO on this site'),
                 help=_('It is a good idea to disable access to WATO completely on the slave site. '
                        'Otherwise a user who does not now about the replication could make local '
                        'changes that are overridden at the next configuration activation.'),
             )),
            ("insecure",
             Checkbox(
                 title=_("Ignore TLS errors"),
                 label=_('Ignore SSL certificate errors'),
                 help=_('This might be needed to make the synchronization accept problems with '
                        'SSL certificates when using an SSL secured connection.'),
             )),
            ("user_login",
             Checkbox(
                 title=_('Direct login to Web GUI allowed'),
                 label=_('Users are allowed to directly login into the Web GUI of this site'),
                 help=_(
                     'When enabled, this site is marked for synchronisation every time a Web GUI '
                     'related option is changed in the master site.'),
             )),
            ("user_sync", self._site_mgmt.user_sync_valuespec()),
            ("replicate_ec",
             Checkbox(
                 title=_("Replicate Event Console config"),
                 label=_("Replicate Event Console configuration to this site"),
                 help=
                 _("This option enables the distribution of global settings and rules of the Event Console "
                   "to the remote site. Any change in the local Event Console settings will mark the site "
                   "as <i>need sync</i>. A synchronization will automatically reload the Event Console of "
                   "the remote site."),
             )),
            ("replicate_mkps",
             Checkbox(
                 title=_("Replicate extensions"),
                 label=_("Replicate extensions (MKPs and files in <tt>~/local/</tt>)"),
                 help=
                 _("If you enable the replication of MKPs then during each <i>Activate Changes</i> MKPs "
                   "that are installed on your master site and all other files below the <tt>~/local/</tt> "
                   "directory will be also transferred to the slave site. Note: <b>all other MKPs and files "
                   "below <tt>~/local/</tt> on the slave will be removed</b>."),
             )),
        ]


@mode_registry.register
class ModeDistributedMonitoring(WatoMode):
    @classmethod
    def name(cls):
        return "sites"

    @classmethod
    def permissions(cls):
        return ["sites"]

    def __init__(self):
        super(ModeDistributedMonitoring, self).__init__()
        self._site_mgmt = watolib.SiteManagementFactory().factory()

    def title(self):
        return _("Distributed Monitoring")

    def buttons(self):
        super(ModeDistributedMonitoring, self).buttons()
        html.context_button(
            _("New connection"), watolib.folder_preserving_link([("mode", "edit_site")]), "new")

    def action(self):
        delete_id = html.request.var("_delete")
        if delete_id and html.transaction_valid():
            self._action_delete(delete_id)

        logout_id = html.request.var("_logout")
        if logout_id:
            return self._action_logout(logout_id)

        login_id = html.request.var("_login")
        if login_id:
            return self._action_login(login_id)

    def _action_delete(self, delete_id):
        configured_sites = self._site_mgmt.load_sites()
        # The last connection can always be deleted. In that case we
        # fall back to non-distributed-WATO and the site attribute
        # will be removed.
        test_sites = dict(configured_sites.items())
        del test_sites[delete_id]

        # Make sure that site is not being used by hosts and folders
        if delete_id in watolib.Folder.root_folder().all_site_ids():
            search_url = html.makeactionuri([
                ("host_search_change_site", "on"),
                ("host_search_site", delete_id),
                ("host_search", "1"),
                ("folder", ""),
                ("mode", "search"),
                ("filled_in", "edit_host"),
            ])
            raise MKUserError(
                None,
                _("You cannot delete this connection. It has folders/hosts "
                  "assigned to it. You can use the <a href=\"%s\">host "
                  "search</a> to get a list of the hosts.") % search_url)


        c = wato_confirm(_("Confirm deletion of site %s") % html.render_tt(delete_id),
                         _("Do you really want to delete the connection to the site %s?") % \
                         html.render_tt(delete_id))
        if c:
            self._site_mgmt.delete_site(delete_id)
            return None

        elif c is False:
            return ""

        return None

    def _action_logout(self, logout_id):
        configured_sites = self._site_mgmt.load_sites()
        site = configured_sites[logout_id]
        c = wato_confirm(_("Confirm logout"),
                         _("Do you really want to log out of '%s'?") % \
                         html.render_tt(site["alias"]))
        if c:
            if "secret" in site:
                del site["secret"]
            self._site_mgmt.save_sites(configured_sites)
            watolib.add_change(
                "edit-site",
                _("Logged out of remote site %s") % html.render_tt(site["alias"]),
                domains=[watolib.ConfigDomainGUI],
                sites=[watolib.default_site()])
            return None, _("Logged out.")

        elif c is False:
            return ""

        else:
            return None

    def _action_login(self, login_id):
        configured_sites = self._site_mgmt.load_sites()
        if html.request.var("_abort"):
            return "sites"

        if not html.check_transaction():
            return

        site = configured_sites[login_id]
        error = None
        # Fetch name/password of admin account
        if html.request.has_var("_name"):
            name = html.request.var("_name", "").strip()
            passwd = html.request.var("_passwd", "").strip()
            try:
                if not html.get_checkbox("_confirm"):
                    raise MKUserError(
                        "_confirm",
                        _("You need to confirm that you want to "
                          "overwrite the remote site configuration."))

                response = watolib.do_site_login(login_id, name, passwd)

                if isinstance(response, dict):
                    if cmk.is_managed_edition() and response["edition_short"] != "cme":
                        raise MKUserError(
                            None,
                            _("The Check_MK Managed Services Edition can only "
                              "be connected with other sites using the CME."))
                    secret = response["login_secret"]
                else:
                    secret = response

                site["secret"] = secret
                self._site_mgmt.save_sites(configured_sites)
                message = _("Successfully logged into remote site %s.") % html.render_tt(
                    site["alias"])
                watolib.log_audit(None, "edit-site", message)
                return None, message

            except watolib.MKAutomationException as e:
                error = _("Cannot connect to remote site: %s") % e

            except MKUserError as e:
                html.add_user_error(e.varname, e)
                error = "%s" % e

            except Exception as e:
                logger.exception()
                if config.debug:
                    raise
                html.add_user_error("_name", error)
                error = (_("Internal error: %s\n%s") % (e, traceback.format_exc())).replace(
                    "\n", "\n<br>")

        wato_html_head(_("Login into site \"%s\"") % site["alias"])
        if error:
            html.show_error(error)

        html.p(
            _("For the initial login into the slave site %s "
              "we need once your administration login for the Multsite "
              "GUI on that site. Your credentials will only be used for "
              "the initial handshake and not be stored. If the login is "
              "successful then both side will exchange a login secret "
              "which is used for the further remote calls.") % html.render_tt(site["alias"]))

        html.begin_form("login", method="POST")
        forms.header(_('Login credentials'))
        forms.section(_('Administrator name'))
        html.text_input("_name")
        html.set_focus("_name")
        forms.section(_('Administrator password'))
        html.password_input("_passwd")
        forms.section(_('Confirm overwrite'))
        html.checkbox(
            "_confirm", False, label=_("Confirm overwrite of the remote site configuration"))
        forms.end()
        html.button("_do_login", _("Login"))
        html.button("_abort", _("Abort"))
        html.hidden_field("_login", login_id)
        html.hidden_fields()
        html.end_form()
        html.footer()
        return False

    def page(self):
        sites = sort_sites(self._site_mgmt.load_sites().items())

        html.div("", id_="message_container")
        with table_element(
                "sites",
                _("Connections"),
                empty_text=_(
                    "You have not configured any local or remotes sites. Multisite will "
                    "implicitely add the data of the local monitoring site. If you add remotes "
                    "sites, please do not forget to add your local monitoring site also, if "
                    "you want to display its data.")) as table:

            for site_id, site in sites:
                table.row()

                self._show_buttons(table, site_id, site)
                self._show_basic_settings(table, site_id, site)
                self._show_livestatus_settings(table, site_id, site)
                self._show_replication_configuration(table, site_id, site)
                self._show_livestatus_status(table, site_id, site)
                self._show_replication_status(table, site_id, site)

        has_replication_sites = any(e[1]["replication"] for e in sites)
        if has_replication_sites:
            html.javascript("cmk.sites.fetch_replication_status();")

    def _show_buttons(self, table, site_id, site):
        table.cell(_("Actions"), css="buttons")
        edit_url = watolib.folder_preserving_link([("mode", "edit_site"), ("edit", site_id)])
        html.icon_button(edit_url, _("Properties"), "edit")

        clone_url = watolib.folder_preserving_link([("mode", "edit_site"), ("clone", site_id)])
        html.icon_button(clone_url, _("Clone this connection in order to create a new one"),
                         "clone")

        delete_url = html.makeactionuri([("_delete", site_id)])
        html.icon_button(delete_url, _("Delete"), "delete")

        if self._site_globals_editable(site_id, site):
            globals_url = watolib.folder_preserving_link([("mode", "edit_site_globals"),
                                                          ("site", site_id)])

            has_site_globals = bool(site.get("globals"))
            title = _("Site specific global configuration")
            if has_site_globals:
                icon = "site_globals_modified"
                title += " (%s)" % (_("%d specific settings") % len(site.get("globals")))
            else:
                icon = "site_globals"

            html.icon_button(globals_url, title, icon)

        if site["replication"]:
            if site.get("secret"):
                logout_url = watolib.make_action_link([("mode", "sites"), ("_logout", site_id)])
                html.icon_button(logout_url, _("Logout"), "autherr")
            else:
                login_url = watolib.make_action_link([("mode", "sites"), ("_login", site_id)])
                html.icon_button(login_url, _("Login"), "authok")

    def _site_globals_editable(self, site_id, site):
        # Site is a remote site of another site. Allow to edit probably pushed site
        # specific globals when remote WATO is enabled
        if watolib.is_wato_slave_site():
            return True

        # Local site: Don't enable site specific locals when no remote sites configured
        if not config.has_wato_slave_sites():
            return False

        return site["replication"] or config.site_is_local(site_id)

    def _show_basic_settings(self, table, site_id, site):
        table.text_cell(_("ID"), site_id)
        table.text_cell(_("Alias"), site.get("alias", ""))

    def _show_livestatus_settings(self, table, site_id, site):
        table.cell(_("Connection"))
        vs_connection = self._site_mgmt.connection_method_valuespec()
        html.write(vs_connection.value_to_text(site["socket"]))

    def _show_replication_configuration(self, table, site_id, site):
        table.text_cell(_("Replication"))
        if not site["replication"]:
            html.icon(_("Replication not enabled for this site"), "disabled")
            return

        html.icon(_("Replication enabled for this site"), "enabled")

        if site.get("replicate_ec"):
            html.icon(_("Replicate Event Console configuration to this site"), "mkeventd")
        if site.get("replicate_mkps"):
            html.icon(_("Replicate extensions"), "mkps")

    def _show_livestatus_status(self, table, site_id, site):
        table.text_cell(_("Livestatus"))

        # The status is fetched asynchronously for all sites. Show a temporary loading icon.
        html.open_div(id_="livestatus_status_%s" % site_id)
        html.icon(
            _("Fetching livestatus status"),
            "reload",
            class_=["reloading", "replication_status_loading"])
        html.close_div()

    def _show_replication_status(self, table, site_id, site):
        table.text_cell(_("Repl. status"))
        html.open_div(id_="replication_status_%s" % site_id)
        if site.get("replication"):
            # The status is fetched asynchronously for all sites. Show a temporary loading icon.
            html.icon(
                _("Fetching replication status"),
                "reload",
                class_=["reloading", "replication_status_loading"])
        html.close_div()


class ModeAjaxFetchSiteStatus(WatoWebApiMode):
    """AJAX handler for asynchronous fetching of the site status"""

    def page(self):
        config.user.need_permission("wato.sites")

        site_states = {}

        sites = watolib.SiteManagementFactory().factory().load_sites().items()
        replication_sites = [e for e in sites if e[1]["replication"]]
        replication_status = ReplicationStatusFetcher().fetch(replication_sites)

        for site_id, site in sites:
            site_states[site_id] = {
                "livestatus": self._render_livestatus_status(site_id, site),
                "replication": self._render_replication_status(site_id, site, replication_status),
            }
        return site_states

    def _render_replication_status(self, site_id, site, replication_status):
        """Check whether or not the replication connection is possible.

        This deals with these situations:
        - No connection possible
        - connection possible but site down
        - Not logged in
        - And of course: Everything is fine
        """
        if not site["replication"]:
            return ""

        status = replication_status[site_id]
        if status.success:
            msg = _("Site is reachable (Version: %s, Edition: %s)") % (status.response.version,
                                                                       status.response.edition)
            return html.render_icon("success", title=msg)
        return html.render_icon("failed", title="%s" % status.response)

    def _render_livestatus_status(self, site_id, site):
        site_status = cmk.gui.sites.state(site_id, {})
        if site.get("disabled", False) is True:
            status = status_msg = "disabled"
        else:
            status = status_msg = site_status.get("state", "unknown")

        if "exception" in site_status:
            message = "%s" % site_status["exception"]
        else:
            message = _("This site is %s") % status_msg

        if message.startswith("[SSL:"):
            status_msg = "TLS error"

        with html.plugged():
            html.status_label(content=status_msg, status=status, title=message)
            return html.drain()


cmk.gui.pages.register_page_handler("wato_ajax_fetch_site_status",
                                    lambda: ModeAjaxFetchSiteStatus().handle_page())

PingResult = NamedTuple("PingResult", [
    ("version", str),
    ("edition", str),
])

ReplicationStatus = NamedTuple("ReplicationStatus", [
    ("site_id", str),
    ("success", bool),
    ("response", TypeVar("ReplicationStatus", PingResult, Exception)),
])


class ReplicationStatusFetcher(object):
    """Helper class to retrieve the replication status of all relevant sites"""

    def __init__(self):
        super(ReplicationStatusFetcher, self).__init__()
        self._logger = logger.getChild("replication-status")

    def fetch(self, sites):
        # type: (List[Tuple[str, Dict]]) -> Dict[str, PingResult]
        self._logger.debug("Fetching replication status for %d sites" % len(sites))
        results_by_site = {}

        # Results are fetched simultaneously from the remote sites
        result_queue = multiprocessing.JoinableQueue()

        processes = []
        for site_id, site in sites:
            process = multiprocessing.Process(
                target=self._fetch_for_site, args=(site_id, site, result_queue))
            process.start()
            processes.append((site_id, process))

        # Now collect the results from the queue until all processes are finished
        while any([p.is_alive() for site_id, p in processes]):
            try:
                result = result_queue.get_nowait()
                result_queue.task_done()
                results_by_site[result.site_id] = result
            except Queue.Empty:
                time.sleep(0.5)  # wait some time to prevent CPU hogs

            except Exception as e:
                logger.exception()
                html.show_error("%s: %s" % (site_id, e))

        self._logger.debug("Got results")
        return results_by_site

    def _fetch_for_site(self, site_id, site, result_queue):
        """Executes the tests on the site. This method is executed in a dedicated
        subprocess (One per site)"""
        self._logger.debug("[%s] Starting" % site_id)
        try:
            # TODO: Would be better to clean all open fds that are not needed, but we don't
            # know the FDs of the result_queue pipe. Can we find it out somehow?
            # Cleanup resources of the apache
            # TODO: Needs to be solved for analzye_configuration too
            #for x in range(3, 256):
            #    try:
            #        os.close(x)
            #    except OSError, e:
            #        if e.errno == 9: # Bad file descriptor
            #            pass
            #        else:
            #            raise

            # Reinitialize logging targets
            log.init_logging()

            result = ReplicationStatus(
                site_id=site_id,
                success=True,
                response=PingResult(**watolib.do_remote_automation(site, "ping", [], timeout=5)),
            )
            self._logger.debug("[%s] Finished" % site_id)
        except Exception as e:
            self._logger.debug("[%s] Failed" % site_id, exc_info=True)
            result = ReplicationStatus(
                site_id=site_id,
                success=False,
                response=e,
            )
        finally:
            result_queue.put(result)
            result_queue.close()
            result_queue.join_thread()
            result_queue.join()


@mode_registry.register
class ModeEditSiteGlobals(GlobalSettingsMode):
    @classmethod
    def name(cls):
        return "edit_site_globals"

    @classmethod
    def permissions(cls):
        return ["sites"]

    def __init__(self):
        super(ModeEditSiteGlobals, self).__init__()
        self._site_id = html.request.var("site")
        self._site_mgmt = watolib.SiteManagementFactory().factory()
        self._configured_sites = self._site_mgmt.load_sites()
        try:
            self._site = self._configured_sites[self._site_id]
        except KeyError:
            raise MKUserError("site", _("This site does not exist."))

        # 2. Values of global settings
        self._global_settings = watolib.load_configuration_settings()

        # 3. Site specific global settings

        if watolib.is_wato_slave_site():
            self._current_settings = watolib.load_configuration_settings(site_specific=True)
        else:
            self._current_settings = self._site.get("globals", {})

    def title(self):
        return _("Edit site specific global settings of %r") % self._site_id

    def buttons(self):
        super(ModeEditSiteGlobals, self).buttons()
        html.context_button(
            _("All Sites"), watolib.folder_preserving_link([("mode", "sites")]), "back")
        html.context_button(
            _("Connection"),
            watolib.folder_preserving_link([("mode", "edit_site"), ("edit", self._site_id)]),
            "sites")

    # TODO: Consolidate with ModeEditGlobals.action()
    def action(self):
        varname = html.request.var("_varname")
        action = html.request.var("_action")
        if not varname:
            return

        config_variable = watolib.config_variable_registry[varname]()
        def_value = self._global_settings.get(varname, self._default_values[varname])

        if action == "reset" and not is_a_checkbox(config_variable.valuespec()):
            c = wato_confirm(
                _("Removing site specific configuration variable"),
                _("Do you really want to remove the configuration variable <b>%s</b> "
                  "of the specific configuration of this site and that way use the global value "
                  "of <b><tt>%s</tt></b>?") %
                (varname, config_variable.valuespec().value_to_text(def_value)))

        else:
            if not html.check_transaction():
                return
            # No confirmation for direct toggle
            c = True

        if c:
            if varname in self._current_settings:
                self._current_settings[varname] = not self._current_settings[varname]
            else:
                self._current_settings[varname] = not def_value

            msg = _("Changed site specific configuration variable %s to %s.") % \
                  (varname, _("on") if self._current_settings[varname] else _("off"))

            self._site.setdefault("globals", {})[varname] = self._current_settings[varname]
            self._site_mgmt.save_sites(self._configured_sites, activate=False)

            watolib.add_change(
                "edit-configvar",
                msg,
                sites=[self._site_id],
                need_restart=config_variable.need_restart(),
            )

            if action == "_reset":
                return "edit_site_globals", msg
            return "edit_site_globals"

        elif c is False:
            return ""

        else:
            return None

    def _edit_mode(self):
        return "edit_site_configvar"

    def page(self):
        html.help(
            _("Here you can configure global settings, that should just be applied "
              "on that site. <b>Note</b>: this only makes sense if the site "
              "is part of a distributed setup."))

        if not watolib.is_wato_slave_site():
            if not config.has_wato_slave_sites():
                html.show_error(
                    _("You can not configure site specific global settings "
                      "in non distributed setups."))
                return

            if not self._site["replication"] and not config.site_is_local(self._site_id):
                html.show_error(
                    _("This site is not the master site nor a replication slave. "
                      "You cannot configure specific settings for it."))
                return

        self._show_configuration_variables(self._groups(show_all=True))
