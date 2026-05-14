import { cookies } from "next/headers";

export async function POST(req: Request) {
    const body = await req.json();

    const response = await fetch(
        "http://localhost:8000/login",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        }
    );

    const data = await response.json();
    console.log("data", data);

    (await cookies()).set("token", data.access_token, {
        httpOnly: true,
        secure: false,
        sameSite: "lax",
        path: "/"
    });

    return Response.json({ success: true });
}