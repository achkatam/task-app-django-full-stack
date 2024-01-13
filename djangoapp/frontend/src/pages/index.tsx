// pages/index.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import EmployeeList from '../components/EmployeeList';
import TaskList from '../components/TaskList';

const IndexPage = () => {
  const [employees, setEmployees] = useState([]);
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const employeesResponse = await axios.get('http://localhost:8000/employees');
        const tasksResponse = await axios.get('http://localhost:8000/tasks');

        setEmployees(employeesResponse.data);
        setTasks(tasksResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <EmployeeList employees={employees} />
      <TaskList tasks={tasks} />
    </div>
  );
};

export default IndexPage;
