<?php
// Smarty ( http://smarty.php.net ) must be available
require("smarty/Smarty.class.php");
// Pages.php declares the availabe pages in $pages and $defaultpage
require("pages.php");
require("acronyms.php");

// create object
$smarty = new Smarty;

$currentpage = $defaultpage;

if(isset($_GET["page"])) {
	$setpage = $_GET["page"];
	if(array_key_exists($setpage,$pages)) {
  	$currentpage = $setpage;
  }
}

$currentfile = $pages[$currentpage]["file"];
$currentname = $pages[$currentpage]["name"];
$index = $_SERVER["PHP_SELF"];

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
$smarty->assign("acronyms",$htmlacronyms);

// display it
$smarty->display("index.tpl");

?>