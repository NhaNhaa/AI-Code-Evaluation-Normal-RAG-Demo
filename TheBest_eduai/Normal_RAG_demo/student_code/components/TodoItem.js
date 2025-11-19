import React from "react";

function TodoItem({ todo, toggleComplete }) { // Missing deleteTodo
  return (
    <li style={{ textDecoration: todo.completed ? "line-through" : "none" }}>
      {todo.text} 
      <button onClick={() => toggleComplete(todo.id)}>Toggle</button>
    </li>
  );
}

export default TodoItem;
