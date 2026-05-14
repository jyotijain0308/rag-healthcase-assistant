import { NextRequest, NextResponse } from "next/server";
import { jwtVerify } from "jose";

const SECRET = new TextEncoder().encode(
  process.env.JWT_SECRET!
);

export default async function middleware(req: NextRequest) {
  const token = req.cookies.get("token")?.value;

  const pathname = req.nextUrl.pathname;

  const protectedRoutes = ["/chat", "/upload"];

  const isProtected = protectedRoutes.some((route) =>
    pathname.startsWith(route)
  );

  if (!isProtected) {
    return NextResponse.next();
  }

  if (!token) {
    return NextResponse.redirect(
      new URL("/login", req.url)
    );
  }

  try {
    await jwtVerify(token, SECRET);

    return NextResponse.next();
  } catch (err: any) {
    console.log("JWT verification failed:", err);

    const response = NextResponse.redirect(
      new URL("/login", req.url)
    );

    response.cookies.delete("token");

    return response;
  }
}

export const config = {
  matcher: ["/chat/:path*", "/upload/:path*"],
};