//==== ==== ==== ==== 
//FUNCTION TO EASLY CREATE DOM ELEMENT, INSERTED IN JQUERY
//==== ==== ==== ==== 	
//TODO - PUT IT INTO A .JS FILE AND IMPORT IT
$.create = function() {
  var ret = [], a = arguments, i, e;
  a = a[0].constructor == Array ? a[0] : a;
  for(i=0; i<a.length; i++) {
    if(a[i+1] && a[i+1].constructor == Object) { // item is element if attributes follow
      e = document.createElement(a[i]);
      $(e).attr(a[++i]); // apply attributes
      if(a[i+1] && a[i+1].constructor == Array) $(e).append($.create(a[++i])); // optional children
      ret.push(e);
    } else { // item is just a text node
      ret.push(document.createTextNode(a[i]));
    }
  }
  return ret;
};	