"use client";

import * as React from "react";
import * as Label from "@radix-ui/react-label";
import { auth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import { login } from "@/services/auth";

export default function LoginForm() {
    const router = useRouter();

    const [email, setEmail] = React.useState("");
    const [password, setPassword] = React.useState("");
    const [loading, setLoading] = React.useState(false);
    const [error, setError] = React.useState("");

    async function handleSubmit(e: React.FormEvent) {
        e.preventDefault();
        setLoading(true);
        setError("");

        try {
            const res = await fetch("/api/login", {
                method: "POST",
                body: JSON.stringify({ email, password })
            });

            const data = await res.json();
            console.log("data", data)

            // store JWT
            if (typeof data !== 'undefined') {
                auth.setToken(data?.access_token);

                // decode role and redirect
                const user = auth.getUser();
                console.log("user", user);
                if (user?.role === "admin") {
                    router.push("/upload");
                } else {
                    router.push("/chat");
                }
            }
        } catch (err: any) {
            setError(err.message || "Login failed");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="w-full max-w-md mx-auto mt-20 p-6 border rounded-xl shadow-sm">
            <h1 className="text-2xl font-semibold mb-6">Login</h1>

            <form onSubmit={handleSubmit} className="space-y-4">

                {/* EMAIL */}
                <div className="space-y-1">
                    <Label.Root className="text-sm font-medium">
                        Email
                    </Label.Root>
                    <input
                        type="email"
                        className="w-full border rounded-md p-2"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>

                {/* PASSWORD */}
                <div className="space-y-1">
                    <Label.Root className="text-sm font-medium">
                        Password
                    </Label.Root>
                    <input
                        type="password"
                        className="w-full border rounded-md p-2"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>

                {/* ERROR */}
                {error && (
                    <p className="text-red-500 text-sm">{error}</p>
                )}

                {/* BUTTON */}
                <button
                    type="submit"
                    disabled={loading}
                    className="w-full bg-black text-white py-2 rounded-md hover:bg-gray-800"
                >
                    {loading ? "Logging in..." : "Login"}
                </button>
            </form>
        </div>
    );
}