<?php
//this takes care of setting the $smarty variable
require('./smarty/smarty-setup.php');

$smarty->assign("test", "Hello, world!");
$smarty->display('index.tpl');
