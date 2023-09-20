function Change() {
    var key = exampleselect.value;
    var d1 = document.getElementById("d1");
    var d2 = document.getElementById("d2");
    var d3 = document.getElementById("d3");
    if(key==1){
      d1.style.display="block";
      d2.style.display="none";
      d3.style.display="none";
    }
    if(key==2){
      d1.style.display="none";
      d2.style.display="block";
      d3.style.display="none";
    }
    if(key==3){
      d1.style.display="none";
      d2.style.display="none";
      d3.style.display="block";
    }
}

function Hide(){
    var d1 = document.getElementById("d1");
    var d2 = document.getElementById("d2");
    var d3 = document.getElementById("d3");
    d1.style.display="none";
    d2.style.display="none";
    d3.style.display="none";
}

function Reveal(){
  var key = exampleselect.value;
  var d1 = document.getElementById("d1");
  var d2 = document.getElementById("d2");
  var d3 = document.getElementById("d3");
  if(key==1){
    d1.style.display="block";
  }
  if(key==2){
    d2.style.display="block";
  }
  if(key==3){
    d3.style.display="block";
  }
}

function selectActive()  {
  const fieldset = document.getElementById('fileex');
  fieldset.disabled = false;
}
  
  function selectDisable()  {
  const fieldset = document.getElementById('fileex');
  fieldset.disabled = true;
}

function fileActive()  {
  const target = document.getElementById('formFile');
  target.disabled = false;
}

function fileDisable()  {
  const target = document.getElementById('formFile');
  target.disabled = true;
}