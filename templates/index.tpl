<!DOCTYPE HTML>
<html>
<head>
    <title>Unsheltered</title>
    <link rel="stylesheet" href="../resources/style.css" type="text/css">
    <meta charset="UTF-8">

    <!-- This stuff will be useful if we make a web app for mobile devices
    <link rel="apple-touch-icon" href="answery-logo.png">
    <meta name="apple-mobile-web-app-capable" content="yes">-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>

        div h1{
            background-color: green;
            width: 100%;
        }

        .shelter {
            background-color: #dae1ed;
            color: black;
            cursor: pointer;
            padding: 10px;
            width: 75%;
            border: none;
            text-align: left;
            outline: none;
            font-size: 16px;
        }

        .active .shelter:hover{
            background-color: #ccc;
        }

        .shelter-info{
            padding: 0 18px;
            display: none;
            overflow: hidden
            background-color: #dae1ed;

        }



    </style>

</head>
<body>

  <div>
    <h1> Unsheltered </h1>
  </div>

  <button class="shelters">Outside In</button>
  <div>
    <p class="shelter-info"> 1132 SW 13th Ave <br>
        Portland, OR 97205 <br>
        Phone: 503.535.3800 <br>
        Fax: 503.223.6837 <br>
  </div>







  <script>
  
    var coll = document.getElementsByClassName("shelters");
    var i;
    for(i = 0; i < coll.length; i++){
        coll[i].addEventListener("click", function(){
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if(content.style.display === "block"){
                content.style.display = "none";
            } else{
                content.style.display = "block";
            }          
            }
        }


  </script>

</body>
</html>
