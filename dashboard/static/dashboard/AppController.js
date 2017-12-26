
function AppController() {
	
	console.log("Initializing app controller");
	
	const loginView = document.querySelector("#loginView");
	this.loginController = new LoginController(this, loginView);
	
	const mainView = document.querySelector("#mainView");
    this.mainController = new MainController(this, mainView);
    
	Controller.call(this, "app", null, [this.loginController, this.mainController], document.body);
	
	this.on("login", obj => {
		this.displayMainView();
	});
	
	this.on("logout", obj => {
		this.displayLoginView()
	});
	
	this.on("unauthorized", obj => {
		this.displayLoginView();
	});
	
	this.displayView();
}

AppController.prototype.displayLoginView = function() {
	this.loginController.show();
	this.mainController.hide();
}

AppController.prototype.displayMainView = function() {
	this.loginController.hide();
	this.mainController.show();
}

AppController.prototype.displayView = function() {
	ServerProxy.isSessionValid()
	.then(value => {
		if (value) {
			this.displayMainView();
		} else {
			this.displayLoginView();
		}
	});
}

AppController.prototype.isSessionValid = function() {

	return Promise.resolve(true);
}

Object.setPrototypeOf(AppController.prototype, Controller.prototype);

