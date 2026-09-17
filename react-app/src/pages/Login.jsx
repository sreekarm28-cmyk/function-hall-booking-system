import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");

    async function handleSubmit(e) {
        e.preventDefault();
        setMessage("");

        try {
            const formData = new URLSearchParams();

            formData.append("username", email);
            formData.append("password", password);

            const response = await fetch(
                "http://127.0.0.1:8000/users/login",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

            if (!response.ok) {
                setMessage(data.detail || "Login failed");
                return;
            }

            localStorage.setItem("token", data.access_token);

            const userResponse = await fetch(
                "http://127.0.0.1:8000/users/me",
                {
                    headers: {
                        "Authorization": `Bearer ${data.access_token}`
                    }
                }
            );

            const userData = await userResponse.json();

            if (!userResponse.ok) {
                setMessage("Could not get user information.");
                return;
            }

            if (userData.role === "hall_owner") {
                navigate("/owner");
            } else if (userData.role === "customer") {
                navigate("/halls");
            } else {
                setMessage("Invalid user role.");
            }

        } catch (error) {
            setMessage("Unable to connect to the server.");
        }
    }

    return (
        <div className="login-page">
            <div className="login-box">
                <h1>Function Hall</h1>

                <p>
                    Welcome back! Please login to continue.
                </p>

                <form onSubmit={handleSubmit}>
                    <label>Email</label>

                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your email"
                        required
                    />

                    <label>Password</label>

                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                        required
                    />

                    <button type="submit">
                        Login
                    </button>

                    {message && <p>{message}</p>}
                </form>
            </div>
        </div>
    );
}

export default Login;