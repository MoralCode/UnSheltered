<?php

require ("vendor/smarty/smarty/libs/Smarty.class.php");

$smarty = new Smarty;

$smarty->setTemplateDir('./templates');
$smarty->setCompileDir('./smarty/templates_c');
$smarty->setCacheDir('./smarty/cache');
$smarty->setConfigDir('./configs');

$smarty->force_compile = true;
$smarty->debugging = false;
$smarty->caching = false;
$smarty->cache_lifetime = 120;

$smarty->assign("test", "Hello, world!");
$smarty->display('index.tpl');
