import { useEffect, useState } from "react";

function Halls() {
    const [halls, setHalls] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const [selectedHall, setSelectedHall] = useState(null);
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [message, setMessage] = useState("");

    useEffect(() => {
        async function fetchHalls() {
            const response = await fetch(
                "http://127.0.0.1:8000/halls/"
            );

            const data = await response.json();

            if (response.ok) {
                // Customer should only see active halls
                setHalls(data.filter((hall) => hall.is_active));
            } else {
                setError(data.detail);
            }

            setLoading(false);
        }

        fetchHalls();
    }, []);

    function handleStartDateChange(e) {
        const date = e.target.value;

        setStartDate(date);

        // Reset end date if it becomes invalid
        if (endDate && new Date(endDate) < new Date(date)) {
            setEndDate("");
        }
    }

    function handleEndDateChange(e) {
        const date = e.target.value;

        if (!startDate) {
            setMessage("Please select a start date first.");
            return;
        }

        const start = new Date(startDate);
        const end = new Date(date);

        const difference =
            (end - start) / (1000 * 60 * 60 * 24);

        if (difference < 0) {
            setMessage("End date cannot be before start date.");
            return;
        }

        if (difference > 1) {
            setMessage("Bookings can only be made for a maximum of 2 days.");
            return;
        }

        setMessage("");
        setEndDate(date);
    }

    async function handleBooking(e) {
        e.preventDefault();

        const token = localStorage.getItem("token");

        const response = await fetch(
            "http://127.0.0.1:8000/bookings/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    hall_id: selectedHall.id,
                    start_date: startDate,
                    end_date: endDate
                })
            }
        );

        const data = await response.json();

        if (response.ok) {
            setMessage("Booking request submitted successfully!");

            setSelectedHall(null);
            setStartDate("");
            setEndDate("");
        } else {
            setMessage(data.detail);
        }
    }

    function closeBookingModal() {
        setSelectedHall(null);
        setStartDate("");
        setEndDate("");
        setMessage("");
    }

    if (loading) {
        return (
            <div className="halls-page">
                <h2>Loading halls...</h2>
            </div>
        );
    }

    if (error) {
        return (
            <div className="halls-page">
                <h2>{error}</h2>
            </div>
        );
    }

    return (
        <div className="halls-page">

            <h1>Find Your Perfect Function Hall</h1>

            <p className="halls-subtitle">
                Choose a hall that fits your event and capacity.
            </p>

            {message && !selectedHall && (
                <div className="customer-message">
                    {message}
                </div>
            )}

            <div className="hall-grid">

                {halls.map((hall) => (
                    <div className="hall-card" key={hall.id}>

                        <div className="hall-card-content">

                            <h2>{hall.name}</h2>

                            <p className="hall-location">
                                📍 {hall.city}
                            </p>

                            <p className="hall-description">
                                {hall.description}
                            </p>

                            <div className="hall-details">

                                <span>
                                    👥 {hall.capacity} people
                                </span>

                                <span>
                                    ₹{hall.price_per_day} / day
                                </span>

                            </div>

                        </div>

                        <button
                            className="book-button"
                            onClick={() => {
                                setSelectedHall(hall);
                                setMessage("");
                            }}
                        >
                            Book Now
                        </button>

                    </div>
                ))}

            </div>

            {halls.length === 0 && (
                <div className="no-halls">
                    <h2>No halls available</h2>
                    <p>
                        There are currently no active halls available for booking.
                    </p>
                </div>
            )}

            {selectedHall && (
                <div className="booking-modal-overlay">

                    <div className="booking-modal">

                        <div className="booking-modal-header">

                            <div>
                                <h2>{selectedHall.name}</h2>

                                <p>
                                    📍 {selectedHall.city}
                                </p>
                            </div>

                            <button
                                className="booking-close-button"
                                onClick={closeBookingModal}
                            >
                                ×
                            </button>

                        </div>

                        <div className="booking-summary">

                            <div>
                                <span>Capacity</span>
                                <strong>
                                    {selectedHall.capacity} people
                                </strong>
                            </div>

                            <div>
                                <span>Price</span>
                                <strong>
                                    ₹{selectedHall.price_per_day} / day
                                </strong>
                            </div>

                        </div>

                        <form onSubmit={handleBooking}>

                            <label>Start Date</label>

                            <input
                                type="date"
                                value={startDate}
                                min={new Date().toISOString().split("T")[0]}
                                onChange={handleStartDateChange}
                                required
                            />

                            <label>End Date</label>

                            <input
                                type="date"
                                value={endDate}
                                min={startDate || new Date().toISOString().split("T")[0]}
                                onChange={handleEndDateChange}
                                required
                            />

                            <p className="booking-limit">
                                Maximum booking duration: 2 days
                            </p>

                            {message && (
                                <p className="booking-error">
                                    {message}
                                </p>
                            )}

                            <div className="booking-modal-actions">

                                <button
                                    type="button"
                                    className="booking-cancel-button"
                                    onClick={closeBookingModal}
                                >
                                    Cancel
                                </button>

                                <button
                                    type="submit"
                                    className="booking-confirm-button"
                                    disabled={!startDate || !endDate}
                                >
                                    Confirm Booking
                                </button>

                            </div>

                        </form>

                    </div>

                </div>
            )}

        </div>
    );
}

export default Halls;