<?php
// Smarty ( http://smarty.php.net ) must be available
require("smarty/Smarty.class.php");
// Pages.php declares the availabe pages in $pages and $defaultpage
require("pages.php");
require("images.php");
require("acronyms.php");

// create object
$smarty = new Smarty;

$currentpage = $defaultpage;
$currentfile = $null;

if(isset($_GET["page"])) {
	$setpage = $_GET["page"];
	if(array_key_exists($setpage,$pages)) {
  	    $currentpage = $setpage;
    }
}

if(isset($_GET["viewimage"])) {
	$setimage = $_GET["viewimage"];
	if(array_key_exists($setimage,$images)) {
  	    $currentimage = $setimage;
    }
}

if($currentimage == $null) {
    $currentfile = $pages[$currentpage]["file"];
    $currentname = $pages[$currentpage]["name"];
}
else {
    $currentfile = $imagetemplate;
    $currentname = $images[$setimage]["name"];
}
$index = $_SERVER["PHP_SELF"];

/*
foreach(array_keys($images) as $imagekey) {
    $fullimages[$imagekey]["file"] = $imagepath . $images[$imagekey]["file"];
    $fullimages[$imagekey]["name"] = $images[$imagekey]["name"];
}
*/
foreach(array_keys($images) as $imagekey) {
    $htmlimages[$imagekey] = "<img src=\"" . $images[$imagekey]["file"] . "\" alt=\"" . $images[$imagekey]["name"] . "\"/>";
}

foreach(array_keys($acronyms) as $acronym) {
	$htmlacronyms[$acronym] = "<acronym title=\"" . $acronyms[$acronym] . "\">" . $acronym . "</acronym>";
}

// set values
$smarty->assign("appname", "Circe");
$smarty->assign("currentname", $currentname);
$smarty->assign("currentpage", $currentpage);
$smarty->assign("currentfile",$currentfile);
//$smarty->assign("datetime", date("D M j G:i:s T Y"));
$smarty->assign("pages",$pages);
$smarty->assign("index",$index);
$smarty->assign("images",$images);
$smarty->assign("htmlimages",$htmlimages);
$smarty->assign("acronyms",$htmlacronyms);
if($currentimage != $null) {
    $smarty->assign("currentimage",$images[$currentimage]);
}

// display it
$smarty->display("index.tpl");

?>
