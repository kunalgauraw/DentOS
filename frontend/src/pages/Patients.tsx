import React, { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { getPatients } from '../services/api';

interface Patient {
  id: number;
  patient_id: string;
  full_name: string;
  mobile: string;
  gender: string;
  age: number | null;
  blood_group: string | null;
  allergies: string | null;
}

const Patients: React.FC = () => {
  const [searchParams] = useSearchParams();
  const [patients, setPatients] = useState<Patient[]>([]);
  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [isLoading, setIsLoading] = useState(true);

  const fetchPatients = async (searchTerm?: string) => {
    setIsLoading(true);
    try {
      const data = await getPatients(searchTerm);
      setPatients(data);
    } catch (error) {
      console.error('Error fetching patients:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    const searchFromUrl = searchParams.get('search');
    if (searchFromUrl) {
      setSearch(searchFromUrl);
      fetchPatients(searchFromUrl);
    } else {
      fetchPatients();
    }
  }, [searchParams]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    fetchPatients(search);
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Patients</h1>
        <Link to="/patients/new" className="btn btn-primary">
          + New Patient
        </Link>
      </div>

      {/* Search */}
      <div className="card">
        <div className="card-body">
          <form onSubmit={handleSearch} className="flex gap-10">
            <input
              type="text"
              className="form-control"
              placeholder="Search by name, mobile, or patient ID..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{ flex: 1 }}
            />
            <button type="submit" className="btn btn-primary">
              Search
            </button>
            {search && (
              <button
                type="button"
                className="btn btn-outline"
                onClick={() => {
                  setSearch('');
                  fetchPatients();
                }}
              >
                Clear
              </button>
            )}
          </form>
        </div>
      </div>

      {/* Patient List */}
      <div className="card">
        <div className="card-body" style={{ padding: 0 }}>
          {isLoading ? (
            <div className="loading">
              <div className="spinner"></div>
            </div>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Patient ID</th>
                  <th>Name</th>
                  <th>Mobile</th>
                  <th>Age/Gender</th>
                  <th>Blood Group</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {patients.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="text-center text-muted" style={{ padding: '40px' }}>
                      {search ? 'No patients found matching your search' : 'No patients registered yet'}
                    </td>
                  </tr>
                ) : (
                  patients.map((patient) => (
                    <tr key={patient.id}>
                      <td>{patient.patient_id}</td>
                      <td>
                        <Link to={`/patients/${patient.id}`}>
                          <strong>{patient.full_name}</strong>
                        </Link>
                        {patient.allergies && (
                          <span className="badge badge-danger" style={{ marginLeft: '10px' }}>
                            Allergies
                          </span>
                        )}
                      </td>
                      <td>{patient.mobile}</td>
                      <td>
                        {patient.age ? `${patient.age} yrs` : '-'} / {patient.gender}
                      </td>
                      <td>{patient.blood_group || '-'}</td>
                      <td>
                        <Link to={`/patients/${patient.id}`} className="btn btn-sm btn-outline">
                          View
                        </Link>
                        <Link
                          to={`/patients/${patient.id}/visit`}
                          className="btn btn-sm btn-primary"
                          style={{ marginLeft: '5px' }}
                        >
                          Consult
                        </Link>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

export default Patients;
