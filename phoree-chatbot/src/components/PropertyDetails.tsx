import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

interface Property {
  title: string;
  price: string;
  bedrooms: number;
  bathrooms: number;
  area: string;
  features: string[];
  image: string;
}

interface PropertyDetailsProps {
  property: Property | null;
}

export default function PropertyDetails({ property }: PropertyDetailsProps) {
  if (!property) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Property Details</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-500">Select a property in chat to view details</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Property Details</CardTitle>
      </CardHeader>
      <CardContent>
        <img 
          src={property.image} 
          alt={property.title} 
          className="w-full h-48 object-cover rounded-md mb-4"
          onError={(e) => {
            e.currentTarget.src = "https://via.placeholder.com/400x300?text=Property+Image"
          }}
        />
        <h3 className="text-xl font-semibold mb-2">{property.title}</h3>
        <p className="text-lg font-bold text-green-600 mb-2">{property.price}</p>
        <div className="flex space-x-2 mb-2">
          <Badge variant="secondary">{property.bedrooms} beds</Badge>
          <Badge variant="secondary">{property.bathrooms} baths</Badge>
          <Badge variant="secondary">{property.area}</Badge>
        </div>
        <h4 className="font-semibold mb-2">Features:</h4>
        <ul className="list-disc list-inside">
          {property.features.map((feature, index) => (
            <li key={index}>{feature}</li>
          ))}
        </ul>
      </CardContent>
    </Card>
  )
}