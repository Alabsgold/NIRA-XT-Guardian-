import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Plus, Users, ArrowRight } from 'lucide-react';

const Dashboard = () => {
    const { api } = useAuth();
    const [families, setFamilies] = useState([]);
    const [showAddModal, setShowAddModal] = useState(false);
    const [newFamilyName, setNewFamilyName] = useState('');

    useEffect(() => {
        fetchFamilies();
    }, []);

    const fetchFamilies = async () => {
        try {
            const res = await api.get('/api/policy/families');
            setFamilies(res.data);
        } catch (error) {
            console.error("Error fetching families", error);
        }
    };

    const handleAddFamily = async (e) => {
        e.preventDefault();
        try {
            await api.post('/api/policy/families', { name: newFamilyName });
            setShowAddModal(false);
            setNewFamilyName('');
            fetchFamilies();
        } catch (error) {
            console.error("Error creating family", error);
        }
    };

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-gray-900">Your Families</h1>
                <button
                    onClick={() => setShowAddModal(true)}
                    className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                    <Plus className="w-5 h-5 mr-2" />
                    Add Family
                </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {families.map((family) => (
                    <Link
                        key={family.id}
                        to={`/family/${family.id}`}
                        className="block bg-white p-6 rounded-lg shadow-sm hover:shadow-md transition-shadow border border-gray-200"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center">
                                <div className="bg-blue-100 p-3 rounded-full">
                                    <Users className="w-6 h-6 text-blue-600" />
                                </div>
                                <h3 className="ml-4 text-lg font-semibold text-gray-900">{family.name}</h3>
                            </div>
                            <ArrowRight className="w-5 h-5 text-gray-400" />
                        </div>
                        <div className="text-sm text-gray-500">
                            <p>Click to manage policies and view logs.</p>
                        </div>
                    </Link>
                ))}
            </div>

            {showAddModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
                    <div className="bg-white rounded-lg p-6 max-w-md w-full">
                        <h2 className="text-xl font-bold mb-4">Add New Family</h2>
                        <form onSubmit={handleAddFamily}>
                            <input
                                type="text"
                                className="w-full border border-gray-300 rounded-md px-3 py-2 mb-4"
                                placeholder="Family Name (e.g. Home, Kids)"
                                value={newFamilyName}
                                onChange={(e) => setNewFamilyName(e.target.value)}
                                required
                            />
                            <div className="flex justify-end space-x-3">
                                <button
                                    type="button"
                                    onClick={() => setShowAddModal(false)}
                                    className="px-4 py-2 text-gray-600 hover:text-gray-800"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                                >
                                    Create
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
