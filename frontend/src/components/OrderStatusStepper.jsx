import { STATUS_FLOW, STATUS_LABELS } from "../constants/orderStatus.js";

export default function OrderStatusStepper({ status }) {
  if (status === "cancelled") {
    return (
      <div className="rounded-lg bg-red-50 px-4 py-3 text-sm font-semibold text-red-600">
        This order was cancelled.
      </div>
    );
  }

  const currentIndex = STATUS_FLOW.indexOf(status);

  return (
    <div className="flex items-center">
      {STATUS_FLOW.map((step, idx) => {
        const done = idx <= currentIndex;
        const isLast = idx === STATUS_FLOW.length - 1;
        return (
          <div key={step} className={`flex items-center ${isLast ? "" : "flex-1"}`}>
            <div className="flex flex-col items-center">
              <div
                className={`flex h-7 w-7 items-center justify-center rounded-full text-xs font-bold ${
                  done ? "bg-zomato text-white" : "bg-gray-200 text-gray-500"
                }`}
              >
                {idx + 1}
              </div>
              <span
                className={`mt-1 w-20 text-center text-[10px] font-medium ${
                  done ? "text-gray-900" : "text-gray-400"
                }`}
              >
                {STATUS_LABELS[step]}
              </span>
            </div>
            {!isLast && (
              <div className={`mx-1 h-0.5 flex-1 ${idx < currentIndex ? "bg-zomato" : "bg-gray-200"}`} />
            )}
          </div>
        );
      })}
    </div>
  );
}
