Controller.all = [];

Controller.byName = function(name) {
	const found = Controller.all.filter(c => c.name == name);
	return found;
}

Controller.add = function(controllers) {
	Controller.all.push(controllers)
}

function Controller(name, parentController, childControllers, rootElement) {
	
	if (parentController && !(parentController instanceof Controller)) {
		throw new TypeError("Parent controller is not of type Controller: " + parentController);
	}
	
	if (childControllers) {
		Controller.add(childControllers)
	}
	
	this.name = name;
	this.listeners = Object.create(null);
	this.parentController = parentController;
	this.childControllers = childControllers;
	this.rootElement = rootElement;
}

Controller.prototype.hide = function() {
	this.rootElement.style.display = "none";
	
	if (this.childControllers) {
		this.childControllers.forEach(c => c.hide());
	}
}

Controller.prototype.show = function(displayType) {
	
	var realDisplayType = displayType ? displayType : "block";
	
	this.rootElement.style.display = realDisplayType;
	
	if (this.childControllers) {
		this.childControllers.forEach(c => c.show());
	}
}

Controller.prototype.dispatchEvent = function(eventName, obj) {
	
	const event = {
			source: this,
			name: eventName,
			info: obj
	};
		
	this.notifyAndPropagate(event);
}

Controller.prototype.notifyAndPropagate = function(event) {
	const handlers = this.listeners[event.name];
	
	if (handlers) {
		const self = this;
		
	
		handlers.forEach(h => {
			let callback = h.bind(this, event);
			setTimeout(function() {
					callback();
			},0);
		});
	}
	
	if (this.parentController) {
		this.parentController.notifyAndPropagate(event);
	}
}

Controller.prototype.on = function(eventName, handler) {
	if (!this.listeners[eventName]) {
		this.listeners[eventName] = [];
	}
	
	this.listeners[eventName].push(handler);
}

