<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8" />

<title>{$appname} [{$currentname}]</title>

<link rel="stylesheet" href="circe.css" type="text/css"/>
<link rel="shortcut icon" href="favicon.ico"/>
</head>
<body>

<div id="header">
<h1 id="appname">
{$appname}
</h1>
</div>

<div id="menu">
<span id="menulist">
{foreach key=key name=pages item=page from=$pages}
{if $smarty.foreach.pages.first == false}
&#8226;
{/if}
{if $key == $currentpage}
<span id="active">
{else}
<span>
{/if}
<a href="{$index}?page={$key}">{$page.name}</a></span>
{/foreach}
</span>
</div>


<div id="content">
{include file="$currentfile"}
</div>

<!--
<div id="footer">
<a href="http://developer.berlios.de/projects/circe/"><img src="http://developer.berlios.de/sflogo.php?group_id=1863&amp;type=1" alt="Hosted by Berlios" title="Hosted by Berlios" id="berlioslogo"/></a>
<span id="leftsection">Generated on {$smarty.now|date_format:"%Y-%m-%d %H:%M:%S"} by <a href="http://smarty.php.net">Smarty</a> v{$smarty.version}</span><br/>
<a href="http://validator.w3.org/check?uri=referer">
<img src="http://www.w3.org/Icons/valid-xhtml10" alt="Valid XHTML 1.0!" class="w3image"/>
</a>
<a href="http://jigsaw.w3.org/css-validator/check/referer" title="Valid CSS 2.0!">
<img src="http://jigsaw.w3.org/css-validator/images/vcss" alt="Valid CSS 2.0!" class="w3image"/>
</a>
</div>
-->

<div id="footer">
<a href="http://developer.berlios.de/projects/circe/"><img src="http://developer.berlios.de/sflogo.php?group_id=1863&amp;type=1" alt="Hosted by Berlios" title="Hosted by Berlios" id="berlioslogo"/></a>
<span id="leftsection">
Generated on {$smarty.now|date_format:"%Y-%m-%d %H:%M:%S"} by <a href="http://smarty.php.net">Smarty</a> v{$smarty.version}
|
<a href="http://validator.w3.org/check?uri=referer">
XHTML 1.0</a>
|
<a href="http://jigsaw.w3.org/css-validator/check/referer" title="Valid CSS 2.0!">
CSS2</a>
</span>
</div>

</body>
</html>