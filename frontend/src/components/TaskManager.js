import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TaskManager = () => {
  const [task, setTask] = useState('');
  const [tasks, setTasks] = useState([]);

  const addTask = async () => {
    const res = await axios.post('http://localhost:5000/tasks/add', { task });
    alert(res.data.message);
    fetchTasks();
  };

  const fetchTasks = async () => {
    const res = await axios.get('http://localhost:5000/tasks/list');
    setTasks(res.data.tasks);
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div>
      <h2>Tasks</h2>
      <input
        type="text"
        value={task}
        onChange={(e) => setTask(e.target.value)}
        placeholder="Enter a new task"
      />
      <button onClick={addTask}>Add Task</button>

      <ul>
        {tasks.map((task, index) => (
          <li key={index}>{task.task}</li>
        ))}
      </ul>
    </div>
  );
};

export default TaskManager;