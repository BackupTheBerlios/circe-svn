<?php
require("parsesvn.php");
$svnfile = "svn.xml";
$svnurl = "http://cia.navi.cx/stats/project/Circe/.xml";

print "Fetching SVN data from $svnurl<br/>";

$remotefile = fopen ($svnurl, "r");
if (!$remotefile) {
    print "Could not open $svnurl<br/>";
    exit;
}
print "File opened, started writing to $svnfile<br/>";
$localfile = fopen($svnfile, "w");
if (!$localfile) {
    print "Could not open $svnfile for writing<br/>";
    fclose($remotefile);
    exit;
}
$totalbytes = 0;
while (!feof ($remotefile)) {
    $buffer = fread ($remotefile, 1024);
    $byteswritten = fwrite($localfile,$buffer);
    if(!$byteswritten) {
        print "Write operation failed<br/>";
        fclose($remotefile);
        fclose($localfile);
        exit;
    }
    $totalbytes += $byteswritten;
}
print "Wrote $totalbytes bytes<br/>";
fclose($remotefile);
fclose($localfile);
print "Operation successful<br/><br/>";
print "Parsing and storing important SVN data<br/>";
$result = writesvn();
if(!$result) {
  print "Failed writing SVN data to file<br/>";
}
else {
  print "Wrote SVN data to file<br/>";
}
?>