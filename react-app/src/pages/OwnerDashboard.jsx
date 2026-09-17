
import { useEffect, useState } from "react";

function OwnerDashboard() {
    const [halls, setHalls] = useState([]);
    const [bookings, setBookings] = useState([]);

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [message, setMessage] = useState("");

    const [showHallModal, setShowHallModal] = useState(false);
    const [editingHall, setEditingHall] = useState(null);

    const [hallName, setHallName] = useState("");
    const [hallAddress, setHallAddress] = useState("");
    const [hallCity, setHallCity] = useState("");
    const [capacity, setCapacity] = useState("");
    const [pricePerDay, setPricePerDay] = useState("");
    const [hallDescription, setHallDescription] = useState("");

    async function fetchData() {
        const token = localStorage.getItem("token");

        try {
            const hallResponse = await fetch(
                "http://127.0.0.1:8000/halls/",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            const hallData = await hallResponse.json();

            if (!hallResponse.ok) {
                setError(
                    hallData.detail || "Unable to fetch halls."
                );
                setLoading(false);
                return;
            }

            setHalls(hallData);

            const bookingResponse = await fetch(
                "http://127.0.0.1:8000/bookings/",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            const bookingData = await bookingResponse.json();

            if (!bookingResponse.ok) {
                setError(
                    bookingData.detail ||
                    "Unable to fetch bookings."
                );
                setLoading(false);
                return;
            }

            setBookings(bookingData);

        } catch (error) {
            setError("Unable to connect to the server.");
        }

        setLoading(false);
    }

    useEffect(() => {
        fetchData();
    }, []);

    function resetHallForm() {
        setHallName("");
        setHallAddress("");
        setHallCity("");
        setCapacity("");
        setPricePerDay("");
        setHallDescription("");
        setEditingHall(null);
    }

    function openCreateHall() {
        resetHallForm();
        setShowHallModal(true);
    }

    function openEditHall(hall) {
        setEditingHall(hall);

        setHallName(hall.name);
        setHallAddress(hall.address);
        setHallCity(hall.city);
        setCapacity(hall.capacity);
        setPricePerDay(hall.price_per_day);
        setHallDescription(hall.description);

        setShowHallModal(true);
    }

    function closeHallModal() {
        setShowHallModal(false);
        resetHallForm();
    }

    // CREATE / EDIT HALL

    async function handleHallSubmit(e) {
        e.preventDefault();

        const token = localStorage.getItem("token");

        const hallData = {
            name: hallName,
            address: hallAddress,
            city: hallCity,
            capacity: Number(capacity),
            price_per_day: Number(pricePerDay),
            description: hallDescription
        };

        try {
            let response;

            if (editingHall) {
                response = await fetch(
                    `http://127.0.0.1:8000/halls/${editingHall.id}`,
                    {
                        method: "PATCH",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`
                        },
                        body: JSON.stringify(hallData)
                    }
                );
            } else {
                response = await fetch(
                    "http://127.0.0.1:8000/halls/",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`
                        },
                        body: JSON.stringify(hallData)
                    }
                );
            }

            const data = await response.json();

            if (!response.ok) {
                setMessage(
                    data.detail || "Unable to save hall."
                );
                return;
            }

            setMessage(
                editingHall
                    ? "Hall updated successfully."
                    : "Hall created successfully."
            );

            closeHallModal();
            fetchData();

        } catch (error) {
            setMessage("Unable to connect to the server.");
        }
    }

    // ACTIVATE / DEACTIVATE HALL

    async function handleHallStatus(hall) {
        const newStatus = !hall.is_active;

        const action = newStatus
            ? "activate"
            : "remove";

        const confirmed = window.confirm(
            `Are you sure you want to ${action} this hall?`
        );

        if (!confirmed) {
            return;
        }

        const token = localStorage.getItem("token");

        try {
            const response = await fetch(
                `http://127.0.0.1:8000/halls/${hall.id}/status`,
                {
                    method: "PATCH",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        is_active: newStatus
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                setMessage(
                    data.detail ||
                    "Unable to update hall status."
                );
                return;
            }

            setMessage(
                newStatus
                    ? "Hall activated successfully."
                    : "Hall removed successfully."
            );

            fetchData();

        } catch (error) {
            setMessage("Unable to connect to the server.");
        }
    }

    // BOOKING ACTION

    async function handleBookingAction(bookingId, action) {
        const actionName =
            action === "confirm"
                ? "confirm"
                : action === "cancel"
                    ? "cancel"
                    : "complete";

        const confirmed = window.confirm(
            `Are you sure you want to ${actionName} this booking?`
        );

        if (!confirmed) {
            return;
        }

        const token = localStorage.getItem("token");

        try {
            const response = await fetch(
                `http://127.0.0.1:8000/bookings/${bookingId}/${action}`,
                {
                    method: "PATCH",
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            const data = await response.json();

            if (!response.ok) {
                setMessage(
                    data.detail ||
                    `Unable to ${actionName} booking.`
                );
                return;
            }

            setMessage(
                `Booking ${actionName}ed successfully.`
            );

            fetchData();

        } catch (error) {
            setMessage("Unable to connect to the server.");
        }
    }

    const pendingBookings = bookings.filter(
        (booking) => booking.status === "PENDING"
    );

    if (loading) {
        return <h2>Loading dashboard...</h2>;
    }

    if (error) {
        return <h2>{error}</h2>;
    }

    return (
        <div className="owner-page">

            <h1>Owner Dashboard</h1>

            <p className="owner-subtitle">
                Manage your function halls and bookings.
            </p>

            {message && (
                <p className="owner-message">
                    {message}
                </p>
            )}

            {/* STATS */}

            <div className="owner-stats">

                <div className="owner-card">
                    <h2>My Halls</h2>
                    <p>
                        {halls.filter(
                            (hall) => hall.is_active
                        ).length}
                    </p>
                </div>

                <div className="owner-card">
                    <h2>Total Bookings</h2>
                    <p>{bookings.length}</p>
                </div>

                <div className="owner-card">
                    <h2>Pending Bookings</h2>
                    <p>{pendingBookings.length}</p>
                </div>

            </div>

            {/* HALLS */}

            <div className="owner-section">

                <div className="section-header">

                    <h2>My Halls</h2>

                    <button
                        className="create-button"
                        onClick={openCreateHall}
                    >
                        + Create Hall
                    </button>

                </div>

                {halls.length === 0 ? (

                    <p>No halls found.</p>

                ) : (

                    <div className="hall-grid">

                        {halls.map((hall) => (

                            <div
                                className="hall-card"
                                key={hall.id}
                            >

                                <h2>{hall.name}</h2>

                                <p>{hall.city}</p>

                                <p>
                                    Capacity: {hall.capacity} people
                                </p>

                                <p>
                                    ₹{hall.price_per_day} / day
                                </p>

                                <p>
                                    Status:{" "}
                                    {hall.is_active
                                        ? "Active"
                                        : "Inactive"}
                                </p>

                                <div className="hall-actions">

                                    <button
                                        className="edit-button"
                                        onClick={() =>
                                            openEditHall(hall)
                                        }
                                    >
                                        Edit
                                    </button>

                                    <button
                                        className={
                                            hall.is_active
                                                ? "remove-button"
                                                : "activate-button"
                                        }
                                        onClick={() =>
                                            handleHallStatus(hall)
                                        }
                                    >
                                        {hall.is_active
                                            ? "Remove"
                                            : "Activate"}
                                    </button>

                                </div>

                            </div>

                        ))}

                    </div>

                )}

            </div>

            {/* BOOKINGS */}

            <div className="owner-section">

                <h2>Bookings</h2>

                {bookings.length === 0 ? (

                    <p>No bookings found.</p>

                ) : (

                    <div className="booking-list">

                        {bookings.map((booking) => (

                            <div
                                className="booking-item"
                                key={booking.id}
                            >

                                <div className="booking-info">

                                    <strong>
                                        #{booking.id}
                                    </strong>

                                    <span>
                                        Hall {booking.hall_id}
                                    </span>

                                    <span>
                                        {booking.start_date}
                                        {" → "}
                                        {booking.end_date}
                                    </span>

                                    <span>
                                        {booking.status}
                                    </span>

                                </div>

                                <div className="booking-actions">

                                    {booking.status === "PENDING" && (
                                        <>
                                            <button
                                                className="confirm-button"
                                                onClick={() =>
                                                    handleBookingAction(
                                                        booking.id,
                                                        "confirm"
                                                    )
                                                }
                                            >
                                                Confirm
                                            </button>

                                            <button
                                                className="remove-button"
                                                onClick={() =>
                                                    handleBookingAction(
                                                        booking.id,
                                                        "cancel"
                                                    )
                                                }
                                            >
                                                Cancel
                                            </button>
                                        </>
                                    )}

                                    {booking.status === "CONFIRMED" && (
                                        <>
                                            <button
                                                className="complete-button"
                                                onClick={() =>
                                                    handleBookingAction(
                                                        booking.id,
                                                        "complete"
                                                    )
                                                }
                                            >
                                                Complete
                                            </button>

                                            <button
                                                className="remove-button"
                                                onClick={() =>
                                                    handleBookingAction(
                                                        booking.id,
                                                        "cancel"
                                                    )
                                                }
                                            >
                                                Cancel
                                            </button>
                                        </>
                                    )}

                                </div>

                            </div>

                        ))}

                    </div>

                )}

            </div>

            {/* CREATE / EDIT HALL MODAL */}

            {showHallModal && (

                <div className="modal-overlay">

                    <div className="modal-box">

                        <div className="modal-header">

                            <h2>
                                {editingHall
                                    ? "Edit Hall"
                                    : "Create New Hall"}
                            </h2>

                            <button
                                className="close-button"
                                onClick={closeHallModal}
                            >
                                ×
                            </button>

                        </div>

                        <form onSubmit={handleHallSubmit}>

                            <label>Hall Name</label>

                            <input
                                type="text"
                                value={hallName}
                                onChange={(e) =>
                                    setHallName(e.target.value)
                                }
                                placeholder="Enter hall name"
                                required
                            />

                            <label>Address</label>

                            <input
                                type="text"
                                value={hallAddress}
                                onChange={(e) =>
                                    setHallAddress(e.target.value)
                                }
                                placeholder="Enter address"
                                required
                            />

                            <label>City</label>

                            <input
                                type="text"
                                value={hallCity}
                                onChange={(e) =>
                                    setHallCity(e.target.value)
                                }
                                placeholder="Enter city"
                                required
                            />

                            <label>Capacity</label>

                            <input
                                type="number"
                                value={capacity}
                                onChange={(e) =>
                                    setCapacity(e.target.value)
                                }
                                placeholder="Enter capacity"
                                min="1"
                                required
                            />

                            <label>Price Per Day</label>

                            <input
                                type="number"
                                value={pricePerDay}
                                onChange={(e) =>
                                    setPricePerDay(e.target.value)
                                }
                                placeholder="Enter price per day"
                                min="0"
                                required
                            />

                            <label>Description</label>

                            <textarea
                                value={hallDescription}
                                onChange={(e) =>
                                    setHallDescription(e.target.value)
                                }
                                placeholder="Enter hall description"
                                rows="3"
                                required
                            />

                            <div className="modal-actions">

                                <button
                                    type="button"
                                    className="cancel-button"
                                    onClick={closeHallModal}
                                >
                                    Cancel
                                </button>

                                <button
                                    type="submit"
                                    className="create-button"
                                >
                                    {editingHall
                                        ? "Save Changes"
                                        : "Create Hall"}
                                </button>

                            </div>

                        </form>

                    </div>

                </div>

            )}

        </div>
    );
}

export default OwnerDashboard;

