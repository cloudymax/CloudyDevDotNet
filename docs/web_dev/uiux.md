---
title: Web Ui Tests
hide:
  - toc
  - navigation
---

<head>
    <style>
       @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300&display=swap');
       .slidecontainer {
         position: relative; 
         background: none;
       }
       .slider { 
         height: 2vh;
         opacity: 0.7;
         border-radius: var(--border-radius);
         width: 100%;
       }
       .slider::-webkit-slider-thumb {
         border-radius: var(--border-radius);
         background: var(--pop);
       }
       .slider::-moz-range-thumb { 
         background: var(--pop);
         width: 1.1vw;
         height: 2.2vh;
       }
       .slider:hover {
         opacity: 1;
         scale: 105%;
         filter: drop-shadow(var(--shadow-x) var(--shadow-y) 3px var(--gray-50)); 
       }
       .flex-container {
         display: flex;
         flex-wrap: nowrap;
         background-color: var(--transparant);
         border-radius: var(--border-radius);
       }
       .flex-container .flex-item {
         background-image: radial-gradient(var(--pop), var(--header) 400% ); 
         width: 10%;
         margin: 1%;
         text-align: center;
         line-height: 75px;
         font-size: calc(var(--emp-multiplier) * var(--font-size));
         border-radius: var(--border-radius);
         opacity: 0.9;
         flex-grow: 1;
       }
       .flex-container .flex-item:hover {
         filter: drop-shadow(var(--shadow-x) var(--shadow-y) 3px var(--shadow));
         scale: 105%;
         opacity: 1;
       }
    </style> 
</head>


> quick test on how well I can nest some simple JS powered UI's inside of mkdocs pages.

<center>
<div class="card-container">
  <div class="card">
    <div class="card-header">
        <h2>Slider</h2>
    </div>
    <div class="card-body">
    <body>
        <div class="slidecontainer">
            <input type="range" min="1" max="100" value="50" class="slider" id="myRange">
        </div>
        <h2>Flexible Boxes</h2>
        <div class="flex-container">
          <div class=flex-item>1</div>
          <div class=flex-item>2</div>
          <div class=flex-item>3</div>  
          <div class=flex-item>4</div>
          <div class=flex-item>5</div>
          <div class=flex-item>6</div>  
          <div class=flex-item>7</div>
          <div class=flex-item>8</div>
        </div>
    </body>
    </div>
    </br>
</div>
</center>