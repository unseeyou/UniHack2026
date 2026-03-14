export class CenterOnUserController extends L.Control {
    constructor(marker, options = null) {
        super(options);

        this.marker = marker;
        this.panningTo = false;
        this.following = true;

        marker.on("move", this.follow);
    }

    onAdd(map) {
        this.map = map;
        map.on("movestart", this.uncentered);

        const container = document.createElement("div");

        const button = this.button = document.createElement("button");
        button.classList = "btn btn-light d-flex align-items-center justify-content-center";
        button.style = "width: 40px; height: 40px; padding: 0";
        button.disabled = this.following;

        button.addEventListener("click", this.center);

        const circle = document.createElement("div");
        circle.style = "width: 15px; height: 15px; background: var(--bs-primary); border-radius: 100%";

        button.appendChild(circle);

        container.appendChild(button);

        return container;
    }

    onRemove(map) {
        this.button.removeEventListener("click", this.center);
    }

    follow = (() => {
        if (this.following) {
            this.panningTo = true;
            this.map.panTo(this.marker.getLatLng());
            this.panningTo = false;
        }
    }).bind(this);

    center = (() => {
        this.panningTo = true;
        this.button.disabled = this.following = true;

        this.map.panTo(this.marker.getLatLng());
        this.panningTo = false;
    }).bind(this);

    uncentered = (() => {
        if (!this.panningTo) this.button.disabled = this.following = false;
    }).bind(this);
}
