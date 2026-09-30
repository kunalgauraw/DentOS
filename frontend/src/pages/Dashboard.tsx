import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getDashboardStats, getRecentPatients, getPendingPayments } from '../services/api';

interface Stats {
  today: {
    visits: number;
    collection: number;
    payments_count: number;
  };
  overall: {
    total_patients: number;
    outstanding: number;
    follow_ups_due: number;
  };
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<Stats | null>(null);
  const [recentPatients, setRecentPatients] = useState<any[]>([]);
  const [pendingPayments, setPendingPayments] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsData, patientsData, paymentsData] = await Promise.all([
          getDashboardStats(),
          getRecentPatients(),
          getPendingPayments(),
        ]);
        setStats(statsData);
        setRecentPatients(patientsData);
        setPendingPayments(paymentsData);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
        <Link to="/patients/new" className="btn btn-primary">
          + New Patient
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid" style={{ marginBottom: '20px' }}>
        <div className="stat-card primary">
          <div className="value">{stats?.overall.total_patients || 0}</div>
          <div className="label">Total Patients</div>
        </div>
        <div className="stat-card success">
          <div className="value">₹{stats?.today.collection?.toLocaleString() || 0}</div>
          <div className="label">Today's Collection</div>
        </div>
        <div className="stat-card warning">
          <div className="value">₹{stats?.overall.outstanding?.toLocaleString() || 0}</div>
          <div className="label">Outstanding</div>
        </div>
        <div className="stat-card primary">
          <div className="value">{stats?.today.visits || 0}</div>
          <div className="label">Today's Visits</div>
        </div>
      </div>

      <div className="grid-2">
        {/* Recent Patients */}
        <div className="card">
          <div className="card-header">
            <span>👥 Recent Patients</span>
            <Link to="/patients" className="btn btn-sm btn-outline">View All</Link>
          </div>
          <div className="card-body" style={{ padding: 0 }}>
            <table className="table">
              <thead>
                <tr>
                  <th>Patient</th>
                  <th>Mobile</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {recentPatients.length === 0 ? (
                  <tr>
                    <td colSpan={3} className="text-center text-muted">
                      No patients yet
                    </td>
                  </tr>
                ) : (
                  recentPatients.map((patient) => (
                    <tr key={patient.id}>
                      <td>
                        <Link to={`/patients/${patient.id}`}>
                          <strong>{patient.full_name}</strong>
                        </Link>
                        <br />
                        <span className="text-muted">{patient.patient_id}</span>
                      </td>
                      <td>{patient.mobile}</td>
                      <td>
                        <Link to={`/patients/${patient.id}/visit`} className="btn btn-sm btn-primary">
                          Consult
                        </Link>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Pending Payments */}
        <div className="card">
          <div className="card-header">
            <span>⚠️ Pending Payments</span>
            <Link to="/billing" className="btn btn-sm btn-outline">View All</Link>
          </div>
          <div className="card-body" style={{ padding: 0 }}>
            <table className="table">
              <thead>
                <tr>
                  <th>Patient</th>
                  <th>Balance</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {pendingPayments.length === 0 ? (
                  <tr>
                    <td colSpan={3} className="text-center text-muted">
                      No pending payments
                    </td>
                  </tr>
                ) : (
                  pendingPayments.map((inv) => (
                    <tr key={inv.id}>
                      <td>
                        <strong>{inv.patient_name}</strong>
                        <br />
                        <span className="text-muted">{inv.invoice_id}</span>
                      </td>
                      <td className="text-danger">₹{inv.balance?.toLocaleString()}</td>
                      <td>
                        <Link to={`/billing/${inv.id}/pay`} className="btn btn-sm btn-primary">
                          Collect
                        </Link>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
