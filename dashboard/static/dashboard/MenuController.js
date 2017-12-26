function MenuController(parentController, rootElement) {
	
	console.log("initializing menu controller");
	
	Controller.call(this, "menu", parentController, [], rootElement);
	
	var logoutButton = rootElement.querySelector("#logout");
	logoutButton.addEventListener("click", this.onLogout.bind(this));
}

Object.setPrototypeOf(MenuController.prototype, Controller.prototype);

MenuController.prototype.onLogout = function() {
	ServerProxy.logout()
	.then(response => {
		this.dispatchEvent('logout', {});
	});
}

MenuController.prototype.show = function() {
	Controller.prototype.show.call(this, "flex");
}
