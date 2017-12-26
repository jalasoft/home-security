var load = function(resource) {
	const script = document.createElement("script");
	script.src = resource;
	script.async = false;
	
	document.head.appendChild(script);
	
}

console.log("Loading controllers.");

load("/static/dashboard/ServerProxy.js");
load("/static/dashboard/Controller.js");
load("/static/dashboard/LoginController.js");
load("/static/dashboard/MenuController.js");
load("/static/dashboard/CameraController.js");
load("/static/dashboard/AppController.js");
load("/static/dashboard/MainController.js");

window.addEventListener("load", e => {
	new AppController();
});


