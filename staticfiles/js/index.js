document.querySelector(".full-year").innerHTML = new Date().getFullYear();

class IndexView {
    constructor() {}
}

class AboutView {
    constructor() {}
}

class ContactView {
    constructor() {}
}

class SearchResultView {
    booking = {
        seats: [],
        route: {
            origin: "",
            pickPoint: "",
            destination: "",
            dropPoint: "",
        },
        trip: {
            tripId: "",
            busId: "",
            busName: "",
        },
    };
    constructor() {
        document
            .querySelector(".amenities-link")
            .addEventListener("click", this.toggleAmenities.bind(this));
        document
            .querySelector("#a-seats-row")
            .addEventListener("click", this.handleASeatClick.bind(this));
        document
            .querySelector("#b-seats-row")
            .addEventListener("click", this.handleASeatClick.bind(this));
        document
            .querySelector(".btn-continue-1")
            .addEventListener("click", this.handlePreview.bind(this));
        document
            .querySelector(".btn-continue-3")
            .addEventListener("click", this.toggleModal.bind(this));
        document
            .querySelector(".btn-continue-5")
            .addEventListener("click", this.populatePassengers.bind(this));
        document
            .getElementById("book-ticket")
            .addEventListener("submit", this.bookTicket.bind(this));
    }

    toggleAmenities(e) {
        let amenities = document.querySelector(".amenities");
        if (amenities.style.display === "none") {
            amenities.style.display = "flex";
        } else {
            amenities.style.display = "none";
        }
    }

    handleASeatClick(evt) {
        if (evt.target.tagName !== "SPAN") {
            return;
        }
        if (evt.target.dataset.status == "booked") {
            return;
        }
        evt.target.classList.add("selected-seat");
        const seatId = evt.target.dataset.id;
        const seatNumber = evt.target.dataset.seat;
        const price = evt.target.dataset.price;
        const origin = evt.target.dataset.origin;
        const destination = evt.target.dataset.destination;
        const busName = evt.target.dataset.bus;
        const busId = evt.target.dataset.busId;
        const tripId = evt.target.dataset.trip;

        const seatIndex = this.booking.seats.findIndex(
            (s) => s.seatId === seatId,
        );
        if (seatIndex >= 0) {
            this.booking.seats.splice(seatIndex, 1);
            localStorage.setItem("booking", JSON.stringify(this.booking));
            evt.target.classList.remove("selected-seat");
            this.applySeatChange(this.booking.seats, price);
            return;
        }

        this.booking.seats.push({
            seatId: seatId,
            seatNumber: seatNumber,
            price: price,
        });
        this.booking.route.origin = origin;
        this.booking.route.destination = destination;
        this.booking.trip.busName = busName;
        (this.booking.trip.busId = busId), (this.booking.trip.tripId = tripId);
        localStorage.setItem("booking", JSON.stringify(this.booking));
        console.log(JSON.parse(localStorage.getItem("booking")));

        this.applySeatChange(this.booking.seats, price);
    }

    applySeatChange(seats = [], price) {
        let strSeats = seats.map((s) => s.seatNumber).join(", ");
        let total = seats.reduce((acc, cur) => (acc += parseInt(cur.price)), 0);
        document.querySelector(".your-seats").innerHTML = strSeats;
        document.querySelector(".normal-seat-aggs").innerHTML = `
            <span class="">Normal</span>
            <span>${this.booking.seats.length} * ${parseInt(price)}</span>
            <span>=KSH ${total}</span>
        `;
        document.querySelector(".cum-total-price").innerHTML = `KES ${total}`;
    }

    handlePreview(evt) {
        if (this.booking.seats.length === 0) {
            return;
        }

        const modalBtn = evt.target.nextElementSibling;

        const pickPoint = document.getElementById("pick-point");
        const dropPoint = document.getElementById("drop-point");
        this.booking.route.pickPoint = pickPoint.value;
        this.booking.route.dropPoint = dropPoint.value;
        localStorage.setItem("booking", JSON.stringify(this.booking));
        let seats = this.booking.seats.map((s) => s.seatNumber).join(", ");
        let count = this.booking.seats.length;
        let total = this.booking.seats.reduce(
            (acc, cur) => (acc += parseInt(cur.price)),
            0,
        );
        let price = this.booking.seats[0].price;

        document.querySelector(".selection-preview").innerHTML = `
            <div>
                    <img src="/static/images/bus_icon.png" width="40px" height="40px" alt="bus">
                </div>
                <div class="flex-col">
                    <span>Bus</span>
                    <span>${this.booking.trip.busName}</span>
                </div>
                <div class="flex-col">
                    <span>Depart</span>
                    <span>${this.booking.route.origin}</span>
                    <span>Boarding</span>
                    <span>${this.booking.route.pickPoint}</span>
                </div>
                <div class="flex-col">
                    <span>Arrive</span>
                    <span>${this.booking.route.destination}</span>
                    <span>Dropping</span>
                    <span>${this.booking.route.dropPoint}</span>
                </div>
                <div class="flex-col">
                    <span>Seats</span>
                    <span>${seats}</span>
                </div>
                <div class="flex-col">
                    <span>Normal:${count} X ${price} = ${total}</span>
                    <span>Total:KES ${total}</span>
                </div>
        `;

        if (modalBtn) {
            modalBtn.click();
        }
    }

    toggleModal(evt) {
        const btn4 = document.querySelector(".btn-continue-4");
        const btn5 = document.querySelector(".btn-continue-5");

        btn4.click();

        setTimeout(() => btn5.click(), 500);
    }

    populatePassengers(evnt) {
        const primarySeat = this.booking.seats[0];
        const otherSeats = this.booking.seats.filter(
            (s) => s.seatNumber !== primarySeat.seatNumber,
        );

        const passengerEl = document.getElementById("passengers");
        const primarySeatEl = `
            <div class="flex justify-between align-center mb-2">
                <span class="text-primary">Primary Passenger</span>
                <span>Seat: <strong>${primarySeat.seatNumber}</strong></span>
            </div>
            <input type="text" required class="form-control mb-2" name="${primarySeat.seatNumber}.fullName" placeholder="Full Name">
            <div class="flex mb-2">
                <div class="mr-2">
                    <input type="radio" name="${primarySeat.seatNumber}.gender" id="${primarySeat.seatNumber}.Male" value="male" />
                <label for="${primarySeat.seatNumber}.Male">Male</label>
                </div>
                <div>
                    <input type="radio" name="${primarySeat.seatNumber}.gender" id="${primarySeat.seatNumber}.Female" value="female" />
                    <label for="${primarySeat.seatNumber}.Female">Female</label>
                </div>
            </div>
            <div class="flex justify-between align-center gap-10">
                <input type="text" name="${primarySeat.seatNumber}.age" placeholder="Age" class="form-control mb-2">
                <select name="${primarySeat.seatNumber}.countrycode" class="form-select mb-2">
                    <option value="+254">+254</option>
                    <option value="+255">+255</option>
                    <option value="+253">+253</option>
                </select>
                <input type="text" name="${primarySeat.seatNumber}.phone_number" placeholder="Mobile Number" class="form-control mb-2" />
            </div>
            <div class="flex gap-10 mb-4">
                <input type="text" name="${primarySeat.seatNumber}.nationality" placeholder="Nationality" class="form-control"/>
                <input type="text" name="${primarySeat.seatNumber}.national_id" placeholder="Identity Number" class="form-control">
            </div>
        `;
        const otherSeatsEl = otherSeats
            .map((seat, index) => {
                return `
                <div class="flex justify-between align-center mb-2">
                <span class="text-info">Other Passenger ${index + 1}</span>
                <span>Seat: <strong>${seat.seatNumber}</strong></span>
                </div>
                <input type="text" required class="form-control mb-2" name="${seat.seatNumber}.fullName" placeholder="Full Name">
                <div class="flex mb-2">
                    <div class="mr-2">
                        <input type="radio" name="${seat.seatNumber}.gender" id="${seat.seatNumber}.Male" value="male" />
                    <label for="${seat.seatNumber}.Male">Male</label>
                    </div>
                    <div>
                        <input type="radio" name="${seat.seatNumber}.gender" id="${seat.seatNumber}.Female" value="female" />
                        <label for="${seat.seatNumber}.Female">Female</label>
                    </div>
                </div>
                <div class="flex justify-between align-center gap-10">
                    <input type="text" name="${seat.seatNumber}.age" placeholder="Age" class="form-control mb-2">
                    <select name="${seat.seatNumber}.countrycode" class="form-select mb-2">
                        <option value="+254">+254</option>
                        <option value="+255">+255</option>
                        <option value="+253">+253</option>
                    </select>
                    <input type="text" name="${seat.seatNumber}.phone_number" placeholder="Mobile Number" class="form-control mb-2" />
                </div>
                <div class="flex gap-10 mb-4">
                    <input type="text" name="${seat.seatNumber}.nationality" placeholder="Nationality" class="form-control"/>
                    <input type="text" name="${seat.seatNumber}.national_id" placeholder="Identity Number" class="form-control">
                </div>
            `;
            })
            .join(" ");

        const total = this.booking.seats.reduce(
            (acc, cur) => (acc += parseInt(cur.price)),
            0,
        );

        passengerEl.innerHTML = primarySeatEl + otherSeatsEl;

        document.getElementById("payable-total").textContent =
            `Proceed To Pay KES ${total}`;
    }

    bookTicket(evt) {
        evt.preventDefault();

        let formData = new FormData(evt.target);
        formData.append("booking", localStorage.getItem("booking"));
        const responseDiv = document.querySelector(".response-msg");

        fetch("/searchresult/", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("data", data);
                responseDiv.classList.add("alert-success");
                responseDiv.classList.remove("alert-danger");
                responseDiv.classList.remove("hidden");
                responseDiv.setAttribute("role", "alert");
                responseDiv.innerText = data.message;
                setTimeout(() => {
                    location.href = `/payment/?reference=${data.payment_reference}&amount=${data.total_payable}&trip=${data.trip}`;
                }, 1000);
            })
            .catch((error) => {
                console.log(error.message);
                responseDiv.classList.add("alert-danger");
                responseDiv.classList.remove("alert-success");
                responseDiv.classList.remove("hidden");
                responseDiv.setAttribute("role", "alert");
                responseDiv.textContent = "Error submitting form.";
            });
    }
}

class GalleryView {
    constructor() {}
}

class ManageTicketView {
    constructor() {}
}

class ManageTicketDetailView {
    constructor() {
        document.getElementById("manageticket")
            .addEventListener("submit", this.rescheduleTicket.bind(this))
    }

    rescheduleTicket(evt) {
        evt.preventDefault()

        const formData = new FormData(evt.target)
        const bookingId = formData.get("booking_id");
        const responseDiv = document.querySelector(".response-msg");

        console.log(bookingId)

        // fetch(`/manageticket/${bookingId}/`, {
        //     method: "POST",
        //     body: formData
        // })
        // .then((response) => response.json())
        // .then((data) => {
        //     console.log("data", data);
        //     responseDiv.classList.add("alert-success");
        //     responseDiv.classList.remove("alert-danger");
        //     responseDiv.classList.remove("hidden");
        //     responseDiv.setAttribute("role", "alert");
        //     responseDiv.innerText = data.message;
        //     // setTimeout(() => {
        //     //     location.href = `/manageticket/${bookingId}`;
        //     // }, 2000);
        // })
        // .catch((error) => {
        //     console.log(error.message);
        //     responseDiv.classList.add("alert-danger");
        //     responseDiv.classList.remove("alert-success");
        //     responseDiv.classList.remove("hidden");
        //     responseDiv.setAttribute("role", "alert");
        //     responseDiv.textContent = `${error.message ? error.message : "Error submitting form."}`;
        // });
    }
}

class SignInView {
    constructor() {}
}

class PaymentView {
    constructor() {
        document
            .getElementById("submit-payment")
            .addEventListener("submit", this.handlePayment.bind(this));
    }

    handlePayment(evt) {
        evt.preventDefault();

        let formData = new FormData(evt.target);
        let amountForm = formData.get("amount");
        let trip = formData.get("trip");
        let reference = formData.get("reference");
        let amountPayable = document.getElementById("amount").dataset.amount;
        const responseDiv = document.querySelector(".response-msg");

        if (amountForm !== amountPayable) {
            responseDiv.classList.add("alert-danger");
            responseDiv.classList.remove("alert-success");
            responseDiv.classList.remove("hidden");
            responseDiv.setAttribute("role", "alert");
            responseDiv.textContent = `Kindly pay ${amountPayable}`;
            return;
        }

        fetch("/payment/", {
            method: "POST",
            body: formData,
        })
            .then((response) => response.json())
            .then((data) => {
                console.log("data", data);
                responseDiv.classList.add("alert-success");
                responseDiv.classList.remove("alert-danger");
                responseDiv.classList.remove("hidden");
                responseDiv.setAttribute("role", "alert");
                responseDiv.innerText = data.message;
                setTimeout(() => {
                    location.href = `/manageticket/?reference=${reference}&trip=${trip}`;
                }, 2000);
            })
            .catch((error) => {
                console.log(error.message);
                responseDiv.classList.add("alert-danger");
                responseDiv.classList.remove("alert-success");
                responseDiv.classList.remove("hidden");
                responseDiv.setAttribute("role", "alert");
                responseDiv.textContent = `${error.message ? error.message : "Error submitting form."}`;
            });
    }
}

const pathname = window.location.pathname;

console.log(pathname);
switch (pathname) {
    case "/":
        new IndexView();
        break;
    case "/about/":
        new AboutView();
        break;
    case "/contact/":
        new ContactView();
        break;
    case "/searchresult/":
        new SearchResultView();
        break;
    case "/gallery/":
        new GalleryView();
        break;
    case "/manageticket/":
        new ManageTicketView();
        break;
    case /^\/manageticket\/\d+$/:
        new ManageTicketDetailView();
        break;
    case "/sign-in/":
        new SignInView();
        break;
    case "/payment/":
        new PaymentView();
        break;
    default:
        break;
}
