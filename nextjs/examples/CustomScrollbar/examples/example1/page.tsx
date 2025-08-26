
import CustomScrollbar from "@/components/CustomScrollbar";

export default function Page() {
  return (
    <div className="h-screen flex items-center justify-center bg-gray-100 p-6">
      <div className="w-96 h-64 bg-white shadow rounded-lg">
        <CustomScrollbar
          className="h-full"
          thumbColor="bg-blue-500 hover:bg-blue-700"
          thumbWidth={2}
        >
          <div className="space-y-4 p-4">
            {Array.from({ length: 40 }).map((_, i) => (
              <p key={i} className="text-gray-700">
                Item {i + 1} — Lorem ipsum dolor sit amet, consectetur
                adipiscing elit. Donec feugiat, sapien nec pretium viverra.
              </p>
            ))}
          </div>
        </CustomScrollbar>
      </div>
    </div>
  );
}
