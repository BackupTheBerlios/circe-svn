<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<meta http-equiv="Content-Type" content="application/xhtml+xml; charset=UTF-8" />

<title>{$appname} [{$currentname}]</title>

<link rel="stylesheet" title="{$appname}" href="circe.css" type="text/css" />

</head>
<body>

<div id="header">
<span id="appname">
{$appname}
</span>
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
<span id="rightsection">Valid <a href="http://validator.w3.org/check/referer">XHTML 1.0</a> and <a href="http://jigsaw.w3.org/css-validator/check/referer">CSS2</a></span>
</div>

</body>
</html>
