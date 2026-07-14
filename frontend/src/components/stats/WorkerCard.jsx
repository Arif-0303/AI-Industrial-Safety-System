function WorkerCard({ sectors }) {

  let workers = 0;

  sectors.forEach((sector) => {
    workers += sector.workers_present;
  });

  return (
    <div className="bg-slate-800 rounded-xl p-5 shadow-lg">

      <h3 className="text-gray-400 text-sm">
        Workers
      </h3>

      <p className="text-3xl font-bold text-blue-400 mt-2">
        {workers}
      </p>

      <p className="text-sm text-gray-500 mt-2">
        Workers On Site
      </p>

    </div>
  );
}

export default WorkerCard;