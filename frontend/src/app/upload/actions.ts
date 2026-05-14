"use server";

import { apiFetch } from "@/lib/api";

export async function processPdfFile(formData: FormData) {
  try {
    const data = await apiFetch("ingest", {
      method: "POST",
      body: formData
    });

    return {
      success: true,
      message: data?.message,
    };
  } catch (error) {
    console.error("PDF processing error:", error);
    return {
      success: false,
      error: "Failed to process PDF",
    };
  }
}
