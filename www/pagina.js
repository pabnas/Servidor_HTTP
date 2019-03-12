function ShowForm()
{
    var forms = document.getElementsByTagName("section");
    forms[0].hidden = false;
}

function HideForm()
{
    var forms = document.getElementsByTagName("section");
    forms[0].hidden = true;

    Nombre.value = "";
    Apellido.value = "";
    Nombre.setAttribute("correcto","");
    Apellido.setAttribute("correcto","");
}

function validar()
{
    var error = false;
    if(Nombre.value == "")
    {
      Nombre.removeAttribute("correcto");
      error = true;
    }
    else
    {
      Nombre.setAttribute("correcto","");
    }

    if(Apellido.value == "")
    {
      Apellido.removeAttribute("correcto");
      error = true;
    }
    else
    {
        Apellido.setAttribute("correcto","");
    }

    if(error == true)
    {
      throw "Error datos invalidos"
    }
}

function addrow(ocultar)
{
    try
    {
      validar();
  		var nombre = Nombre.value;
  		var apellido = Apellido.value;
  		var facultad = Facultades.value;
  		var row = "<tr><td>"+nombre+"</td><td>"+apellido +"</td><td>"+facultad + "</td><td> <input type=image src=\"borrar.png\" width=\"10\" height=\"10\" onclick=\"remove_row(this)\" >"  + "</td></tr>";
  		var elemento = document.createElement("TR");
  		elemento.innerHTML=row;
	    document.getElementById("Lista").appendChild(elemento);
      if(ocultar == true) HideForm();
    }
    catch(error)
    {
        alert(error);
    }
}

function remove_row(t)
{
    var td = t.parentNode;
    var tr = td.parentNode;
    var table = tr.parentNode;
    table.removeChild(tr);
}
