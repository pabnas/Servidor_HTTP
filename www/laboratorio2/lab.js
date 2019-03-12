function cambio(t)
{
  if(t.id == "bombillo")
  {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function()
    {
      if (this.readyState == 4 && this.status == 200)
      {
          t.setAttribute("state", this.responseText);
      }
    };
    xhttp.open("GET", "b.bool", true);
    xhttp.send();
  }
}

function pedir_temp_digital()
{
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function()
  {
    if (this.readyState == 4 && this.status == 200)
    {
        T_digital.setAttribute("state", this.responseText);
    }
  };
  xhttp.open("GET", "t_d.bool", true);
  xhttp.send();
}

fade_vent.oninput = function()
{
},

fade_led.oninput = function()
{
},

window.onload = function()
{
  setInterval(pedir_temp_digital, 1000);
}
