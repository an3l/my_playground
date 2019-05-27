var h1=document.querySelector("h1");
h1.style.color="pink";

// Select body
var body=document.querySelector("body");
var isBlue=false;

//setInterval(f, ms)
setInterval(function(){
	if (!isBlue){
		body.style.background="white";
	}
	else{
		body.style.background="#3498db";
	}
	isBlue=!isBlue;
}, 1000);


//var idName= document.getElementById("hl"); //alternative
var tag=document.querySelector("#hl"); //takes CSS style selector

//var classNames= document.getElementsByClassName("bolded"); // node list htmlcollection -> array like
// classNames.length, classNames[0] but not forEach
// Alternative
var class_=document.querySelector(".bolded"); // returns 1 match (first)
var all_class=document.querySelectorAll(".bolded"); //returns all

var tagName= document.getElementsByTagName("li");// li => 3 li's
var body_= document.getElementsByTagName("body")[0];


var h1=document.querySelector("h1");
h1.addEventListener("click", function(){
	console.log("KLik");
});

// document.URL
// document.links
// document.body
// document.head

// document.getElementById()
// document.getElementSByClassName()
// document.getElementsByTagName()
// document.querySelector()
// document.querySelectorAll()

//alert("Hi!");
//var username= prompt("Your name ? ");
//console.log("Great to meet you "+username);

//patatap.com
// https://codepen.io/ // html, css, javascript
