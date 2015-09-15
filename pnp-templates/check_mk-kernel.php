<?php
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2015             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# Copyright by Mathias Kettner and Mathias Kettner GmbH.  All rights reserved.
#
# Check_MK is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.
#
# Check_MK is  distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY;  without even the implied warranty of
# MERCHANTABILITY  or  FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have  received  a copy of the  GNU  General Public
# License along with Check_MK.  If  not, email to mk@mathias-kettner.de
# or write to the postal address provided at www.mathias-kettner.de

$subtype = substr($servicedesc, 7);
if ($subtype == "pgmajfault" || $subtype == "Major_Page_Faults") {
  $title = "Major Page Faults";
  $vertical = "faults / sec";
  $format = "%5.1lf/s";
  $upto = "500";
  $color = "20ff80";
  $line = "10a040";
}
else if ($subtype == "ctxt" || $subtype == "Context_Switches") {
  $title = "Context Switches";
  $vertical = "switches / sec";
  $format = "%5.1lf/s";
  $upto = "50000";
  $color = "80ff20";
  $line = "40a010";
}
else if ($subtype == "processes" || $subtype == "Process_Creations") {
  $title = "Process creation";
  $vertical = "new processes / sec";
  $format = "%5.1lf/s";
  $upto = "100";
  $color = "ff8020";
  $line = "a04010";
}
else {
  $title = "Kernel counter $subtype";
  $vertical = "per sec";
  $format = "%3.0lf";
  $upto = "100";
  $color = "ffff20";
  $line = "90a010";
}

$opt[1] = " --vertical-label \"$vertical\" -X0 -l 0 -u $upto --title \"$hostname: $title\" ";

$def[1] = "DEF:var1=$RRDFILE[1]:$DS[1]:MAX ";
$def[1] .= "AREA:var1#$color:\"$title\:\" ";
$def[1] .= "LINE1:var1#$line:\"\" ";
$def[1] .= "GPRINT:var1:LAST:\"Current\: $format\" ";
if ($WARN[1])
    $lf = "\\n";
else
    $lf = "";

$def[1] .= "GPRINT:var1:MAX:\"Maximum\: $format\" ";
$def[1] .= "GPRINT:var1:AVERAGE:\"Average\: $format$lf\" ";
if ($WARN[1]) {
 $def[1] .= "HRULE:$WARN[1]#FFFF00:\"Warning\: $WARN[1]/s\" ";
 $def[1] .= "HRULE:$CRIT[1]#FF0000:\"Critical\: $CRIT[1]/s\" ";
}
?>
