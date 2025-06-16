"use client";

import { Dialog } from "@headlessui/react";

export default function StreetModal({
  isOpen,
  onClose,
  street,
}: {
  isOpen: boolean;
  onClose: () => void;
  street: any;
}) {
  if (!street) return null;

  return (
    <Dialog open={isOpen} onClose={onClose} className="relative z-50">
      <div className="fixed inset-0 bg-black/30" aria-hidden="true" />
      <div className="fixed inset-0 z-[1000] flex items-center justify-center">
        <Dialog.Panel className="bg-white p-6 text-black rounded-lg shadow-xl w-[400px]">
          <Dialog.Title className="text-lg font-bold mb-2">
            Straße: {street.name}
          </Dialog.Title>
          <p>Status: {street.status}</p>
          <p>Länge: {street.length} m</p>

          <button
            onClick={onClose}
            className="mt-4 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Schließen
          </button>
        </Dialog.Panel>
      </div>
    </Dialog>
  );
}
