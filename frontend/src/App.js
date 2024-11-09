// src/App.js
import React, { useState } from "react";
import axios from "axios";

function App() {
    const [formData, setFormData] = useState({
        Pclass: "",
        Sex: "",
        Age: "",
        Fare: ""
    });
    const [prediction, setPrediction] = useState(null);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post("http://localhost:8000/predict", formData);
            setPrediction(response.data.Survived ? "Survived" : "Did not survive");
        } catch (error) {
            console.error("Error making prediction", error);
        }
    };

    return (
        <div>
            <h1>Titanic Survival Predictor</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Class:
                    <input type="number" name="Pclass" value={formData.Pclass} onChange={handleChange} />
                </label>
                <label>
                    Sex:
                    <select name="Sex" value={formData.Sex} onChange={handleChange}>
                        <option value="">Select</option>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>
                </label>
                <label>
                    Age:
                    <input type="number" name="Age" value={formData.Age} onChange={handleChange} />
                </label>
                <label>
                    Fare:
                    <input type="number" name="Fare" value={formData.Fare} onChange={handleChange} />
                </label>
                <button type="submit">Predict</button>
            </form>
            {prediction && <h2>Prediction: {prediction}</h2>}
        </div>
    );
}

export default App;
