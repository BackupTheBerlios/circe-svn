<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8" />

<title>{$appname} [{$currentname}]</title>

<link rel="stylesheet" title="{$appname}" href="circe.css" type="text/css" />
</head>
<body>

<div id="header">
<h1 id="appname">
{$appname}
</h1>
</div>

<div id="menu">
<ul id="menulist">
{foreach key=key name=pages item=page from=$pages}
{if $key == $currentpage}
<li id="active">
{else}
<li>
{/if}
<a href="{$index}?page={$key}">&nbsp;{$page.name}</a>
</li>
{/foreach}
</ul>
</div>

<div id="content">
{include file="$currentfile"}
</div>

<div id="footer">

<span id="leftsection">Generated on {$smarty.now|date_format:"%Y-%m-%d %H:%M:%S"} by <a href="http://smarty.php.net">Smarty</a> v{$smarty.version}</span>
<br/>
<span class="w3cbutton3">
<a href="http://validator.w3.org/check/referer">
<span class="w3c">W3C</span>
<span>XHTML 1.0</span>
</a>
</span>
<span class="w3cbutton3">
<a href="http://jigsaw.w3.org/css-validator/check/referer">
<span class="w3c">W3C</span>
<span>CSS2</span>
</a>
</span>
<br/>
<a href="https://developer.berlios.de/projects/circe/"><img src="http://developer.berlios.de/sflogo.php?group_id=1863&amp;type=1" alt="Hosted by Berlios" title="Hosted by Berlios" id="berlioslogo"/></a>
</div>

</body>
</html>