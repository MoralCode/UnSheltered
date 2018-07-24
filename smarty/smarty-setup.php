<?php // load Smarty library
require 'vendor/smarty/smarty/libs/Smarty.class.php';

class Smarty_Setup extends Smarty {

   function __construct()
   {
        parent::__construct();

        $this->setTemplateDir('templates/');
        $this->setCompileDir('./templates_c');
        $this->setConfigDir('./');
        $this->setCacheDir('./caches/');


		// #########################
		// #        CACHING        #
		// #########################

		//A $caching value of 1 tells Smarty to use the current $cache_lifetime variable to determine if cache has expired
		//A value of 2 tells Smarty to use the $cache_lifetime value at the time the cache was generated.
      	$this->caching = false;
        $this->setCacheLifetime(21600);// in seconds, (3600 = 1 hour | 21,600 = 6 hours)
        //$this->caching = Smarty::CACHING_OFF;

        //uncomment the following line to clear all caches
        //$this->clearAllCache();
        
		// ###########################
		// #        COMPILING        #
        // ###########################
        
		//Upon each invocation of the PHP application, Smarty tests
		//to see if the current template has changed since the last time
		//it was compiled. If it has changed, it recompiles that template.
        $this->compile_check = true;
        
		//This forces Smarty to (re)compile templates on every invocation
		//and overrides $compile_check. defaults to false
		//$this->force_compile = TRUE;
   }
}


	//make custom instance of smarty availible in php sessions
	// session_start();
    // $_SESSION["smarty"] = new Smarty_Setup();


  // in case the $_SESSION thing doesnt work, use this
  $smarty = new Smarty_Setup();



//uncomment this line to test smarty installation
//$smarty->testInstall();

//uncomment this line to show the debug window
//$smarty->debugging = true;
?>
