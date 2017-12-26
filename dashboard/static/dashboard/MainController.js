function MainController(parentController, rootElement) {
	
	console.log("Initializing main controller");

    var headerRoot = rootElement.querySelector("#mainView #header");
    var menuController = new MenuController(this, headerRoot);
    	
	var allRefreshes = rootElement.querySelectorAll("*[data-tile-type = 'camera']");
    var cameraControllers = Array.prototype.map.call(allRefreshes, d => new CameraController(this, d));
    
    var childControllers = [menuController, ...cameraControllers];
    
    Controller.call(this, "main", parentController, childControllers, rootElement);
}

Object.setPrototypeOf(MainController.prototype, Controller.prototype);
