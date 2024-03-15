using MeteorShowerIdentification.Rendering.Astrodynamics;
using MeteorShowerIdentification.Rendering.Geometry;
using Microsoft.UI;

namespace MeteorShowerIdentification.Rendering;
internal class CelestialBody
{
    public Microsoft.UI.Xaml.Shapes.Path OrbitPath { get; }
    private readonly Orbit _orbit;
    private readonly float _size;
    private readonly string _name;

    public Brush OrbitStroke { get => OrbitPath.Stroke; set => OrbitPath.Stroke = value; }
    public double OrbitStrokeThickness { get => OrbitPath.StrokeThickness; set => OrbitPath.StrokeThickness = value; }

    public CelestialBody(string name, Orbit orbit, float size)
    {
        _name = name;
        OrbitPath = new Microsoft.UI.Xaml.Shapes.Path() { Stroke = new SolidColorBrush(Colors.Wheat), StrokeDashArray = [1, 10] };
        _orbit = orbit;
        _size = size;
    }

    public void Render(Geometry.Projection perspective, Vector offset, float scale)
    {
        GeometryGroup _geometry = new();
        _geometry.DrawOrbit(perspective, _orbit, offset, scale);
        Vector position = new(_orbit.SemiMajorAxis, 0);
        position = position.Project(perspective);
        EllipseGeometry body = new() { Center = new Windows.Foundation.Point(position.X, position.Y), RadiusX = scale * _size, RadiusY = scale * _size };
        _geometry.Children.Add(body);
        OrbitPath.Data = _geometry;
    }

    public override string ToString()
    {
        return _name;
    }
}
