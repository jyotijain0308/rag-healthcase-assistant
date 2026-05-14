// hooks/useAuth.ts
"use client";

import { useEffect, useState } from "react";

export function useAuth() {
    const [user, setUser] = useState(null);

    useEffect(() => {
        fetch("/api/me")
            .then((r) => r.json())
            .then(setUser);
    }, []);

    return user;
}