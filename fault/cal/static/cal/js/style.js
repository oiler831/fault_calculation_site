function linefieldsetDisable()  {
  const fieldset = document.getElementById('linefieldset');
  fieldset.disabled = true;
}

function linefieldsetActive() {
  const fieldset = document.getElementById('linefieldset');
  fieldset.disabled = false;
}

function busActive()  {
  const target = document.getElementById('bus1');
  target.disabled = false;
}

function busDisable()  {
  const target = document.getElementById('bus1');
  target.disabled = true;
}

function Change() {
    var key = test.value;
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