// +------------------------------------------------------------------+
// |             ____ _               _        __  __ _  __           |
// |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
// |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
// |           | |___| | | |  __/ (__|   <    | |  | | . \            |
// |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
// |                                                                  |
// | Copyright Mathias Kettner 2017             mk@mathias-kettner.de |
// +------------------------------------------------------------------+
//
// This file is part of Check_MK.
// The official homepage is at http://mathias-kettner.de/check_mk.
//
// check_mk is free software;  you can redistribute it and/or modify it
// under the  terms of the  GNU General Public License  as published by
// the Free Software Foundation in version 2.  check_mk is  distributed
// in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
// out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
// PARTICULAR PURPOSE. See the  GNU General Public License for more de-
// ails.  You should have  received  a copy of the  GNU  General Public
// License along with GNU Make; see the file  COPYING.  If  not,  write
// to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
// Boston, MA 02110-1301 USA.

#ifndef ListenSocket_h
#define ListenSocket_h

#include <string>
#include "types.h"

class Logger;
class WinApiInterface;

struct SocketHandleTraits {
    using HandleT = SOCKET;
    static HandleT invalidValue() { return INVALID_SOCKET; }

    static void closeHandle(HandleT value, const WinApiInterface &winapi) {
        winapi.closesocket(value);
    }
};

using SocketHandle = WrappedHandle<SocketHandleTraits>;

class ListenSocket {
public:
    ListenSocket(int port, const only_from_t &source_whitelist,
                 bool supportIPV6, Logger *logger,
                 const WinApiInterface &winapi);

    bool supportsIPV4() const;
    bool supportsIPV6() const;

    SocketHandle acceptConnection() const;

    sockaddr_storage address(SOCKET connection) const;

private:
    SOCKET init_listen_socket(int port);
    bool check_only_from(const SOCKADDR &ip) const;
    SOCKET RemoveSocketInheritance(SOCKET oldsocket) const;

    Logger *_logger;
    const WinApiInterface &_winapi;
    const bool _use_ipv6;
    SocketHandle _socket;
    const only_from_t _source_whitelist;
    bool _supports_ipv4;
};

#endif  // ListenSocket_h
