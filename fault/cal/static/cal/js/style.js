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
