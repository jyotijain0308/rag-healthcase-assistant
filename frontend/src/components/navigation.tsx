"use client";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/use-auth";

export const Navigation = () => {
  const user = useAuth();

  if (!user) {
    return <div></div>;
  }

  async function logout() {
    await fetch("/api/logout", { method: "POST" });
    window.location.href = "/login";
  }

  function login() {
    window.location.href = "/login";
  }

  const getAuthButtons = () => {
    if (user) {
      return <Button variant="outline" onClick={logout}>Sign Out</Button>
    } else {
      return <Button variant="ghost" onClick={login}>Sign In</Button>
    }
  }

  return (
    <nav className="border-b">
      <div className="flex container h-16 items-center justify-between px-4  mx-auto">
        <div className="text-xl font-semibold">RAG Chatbot</div>
        <div className="flex gap-2">
          {getAuthButtons()}
        </div>
      </div>
    </nav>
  );
};
