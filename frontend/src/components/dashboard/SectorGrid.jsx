import SectorCard from "../cards/SectorCard";

function SectorGrid({ sectors }) {

  if (!sectors || sectors.length === 0) {
    return (
      <p className="text-gray-400 text-lg">
        Loading sector data...
      </p>
    );
  }

  return (
    <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-6">
      {sectors.map((sector) => (
        <SectorCard
          key={sector.id}
          sector={sector}
        />
      ))}
    </div>
  );
}

export default SectorGrid;