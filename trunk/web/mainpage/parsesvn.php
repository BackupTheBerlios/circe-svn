<?php
require("xmltoarray.php");
//require("duration.php");
// Parses SVN data and stores it inside a file called svn.tmp
$svntmpfile = "svn.tmp";

function query_str ($params) {
    $str = '';
    foreach ($params as $key => $value) {
        $str .= (strlen($str) < 1) ? '' : '&';
        $str .= $key . '=' . rawurlencode($value);
    }
    return ($str);
}

function saveArray($arr)
{
    global $svntmpfile;
    $fp = fopen($svntmpfile, "w");
    if(!$fp) {
        print "Unable to write to $svntmpfile<br/>";
        return false;
    }
    $qstr = query_str($arr);
    fputs($fp,$qstr);
    /*
    foreach(array_keys($arr) as $item) {
        fputs($fp, trim($arr[$item]) . "\n");
    }
    */
    /*
    for ($ii = 0; $ii < count($arr); $ii++)  
    {
        fputs($fp, $arr[$ii]);
    }
    */
    fclose ($fp);
    return true;
}

function loadArray()
{
    global $svntmpfile;
    $arr = array();
    $fp = fopen($svntmpfile, "r");
    if(!$fp) {
        print "Unable to read from $svntmpfile<br/>";
        return false;
    }
    //while (!feof($fp))
    //{
    $in = fgets($fp, 4094);
    parse_str($in,$arr);
    //$arr[] = trim($in);
    //}
    fclose ($fp);
    return $arr;
}

function writesvn() {
    print "Parsing SVN data<br/>";
    $svnarray = xmlFileToArray("svn.xml");
    if(!$svnarray) {
        // Couldn't parse SVN, somehow
        print "Couldn't parse SVN data<br/>";
        return false;
    }
    else {
        $svndata = array();
        $svn_commit = $svnarray["recentmessages"]["message"][0]["body"]["commit"];
        $svndata["revision"] = $svn_commit["revision"];
        $svndata["author"] = $svn_commit["author"];
        $svndata["log"] = $svn_commit["log"];
        $svndata["timestamp"] = $svnarray["recentmessages"]["message"][0]["timestamp"];
        //$svndata["ago"] = time() - $svndata["timestamp"];
        //$svndata["ago_format"] = Duration::toString($svndata["ago"]);
        print "Revision: " . $svndata["revision"] . "<br/>";
        print "Writing SVN data to file $svntmpfile<br/>";
        return saveArray($svndata);
    }
}
function readsvn() {
    //return loadArray();
    return loadArray();
}
?>