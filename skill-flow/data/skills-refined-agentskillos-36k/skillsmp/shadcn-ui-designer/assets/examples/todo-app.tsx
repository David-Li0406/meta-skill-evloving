// Complete Todo App Example with shadcn/ui
// Install required components: npx shadcn@latest add card checkbox button input dialog label

"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Plus, Trash2 } from "lucide-react"

interface Todo {
  id: string
  title: string
  description: string
  completed: boolean
}

export default function TodoApp() {
  const [todos, setTodos] = useState<Todo[]>([])
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [newTodo, setNewTodo] = useState({ title: "", description: "" })

  const addTodo = () => {
    if (!newTodo.title.trim()) return

    const todo: Todo = {
      id: crypto.randomUUID(),
      title: newTodo.title,
      description: newTodo.description,
      completed: false,
    }

    setTodos([...todos, todo])
    setNewTodo({ title: "", description: "" })
    setIsDialogOpen(false)
  }

  const toggleTodo = (id: string) => {
    setTodos(todos.map((todo) =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ))
  }

  const deleteTodo = (id: string) => {
    setTodos(todos.filter((todo) => todo.id !== id))
  }

  const activeTodos = todos.filter((todo) => !todo.completed)
  const completedTodos = todos.filter((todo) => todo.completed)

  return (
    <div className="container mx-auto max-w-2xl p-6">
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl">My Tasks</CardTitle>
              <CardDescription>
                {activeTodos.length} active, {completedTodos.length} completed
              </CardDescription>
            </div>
            <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
              <DialogTrigger asChild>
                <Button>
                  <Plus className="mr-2 h-4 w-4" />
                  Add Task
                </Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Create New Task</DialogTitle>
                  <DialogDescription>
                    Add a new task to your todo list
                  </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  <div className="grid gap-2">
                    <Label htmlFor="title">Title</Label>
                    <Input
                      id="title"
                      placeholder="Enter task title"
                      value={newTodo.title}
                      onChange={(e) =>
                        setNewTodo({ ...newTodo, title: e.target.value })
                      }
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="description">Description</Label>
                    <Input
                      id="description"
                      placeholder="Enter task description (optional)"
                      value={newTodo.description}
                      onChange={(e) =>
                        setNewTodo({ ...newTodo, description: e.target.value })
                      }
                    />
                  </div>
                </div>
                <DialogFooter>
                  <Button
                    variant="outline"
                    onClick={() => setIsDialogOpen(false)}
                  >
                    Cancel
                  </Button>
                  <Button onClick={addTodo}>Create</Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </div>
        </CardHeader>
        <CardContent>
          {todos.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <p className="text-muted-foreground mb-4">
                No tasks yet. Create your first task to get started!
              </p>
              <Button variant="outline" onClick={() => setIsDialogOpen(true)}>
                <Plus className="mr-2 h-4 w-4" />
                Add Your First Task
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Active Todos */}
              {activeTodos.length > 0 && (
                <div className="space-y-2">
                  {activeTodos.map((todo) => (
                    <Card key={todo.id} className="hover:bg-accent/50 transition-colors">
                      <CardContent className="flex items-start gap-3 p-4">
                        <Checkbox
                          checked={todo.completed}
                          onCheckedChange={() => toggleTodo(todo.id)}
                          className="mt-1"
                        />
                        <div className="flex-1 space-y-1">
                          <p className="font-medium leading-none">{todo.title}</p>
                          {todo.description && (
                            <p className="text-sm text-muted-foreground">
                              {todo.description}
                            </p>
                          )}
                        </div>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => deleteTodo(todo.id)}
                          className="h-8 w-8"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}

              {/* Completed Todos */}
              {completedTodos.length > 0 && (
                <div className="space-y-2">
                  <p className="text-sm font-medium text-muted-foreground">
                    Completed
                  </p>
                  {completedTodos.map((todo) => (
                    <Card key={todo.id} className="opacity-60">
                      <CardContent className="flex items-start gap-3 p-4">
                        <Checkbox
                          checked={todo.completed}
                          onCheckedChange={() => toggleTodo(todo.id)}
                          className="mt-1"
                        />
                        <div className="flex-1 space-y-1">
                          <p className="font-medium leading-none line-through">
                            {todo.title}
                          </p>
                          {todo.description && (
                            <p className="text-sm text-muted-foreground line-through">
                              {todo.description}
                            </p>
                          )}
                        </div>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => deleteTodo(todo.id)}
                          className="h-8 w-8"
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
