using MeteorShowerIdentification.Rendering.Geometry;

namespace MeteorShowerIdentification.Rendering;
internal static class Draw
{
    public static void DrawOrbit(this GeometryGroup group, Geometry.Projection perspective, Astrodynamics.Orbit orbit, Geometry.Vector offset, float scale = 1)
    {
        Ellipse o = orbit.AsEllipse();
        o = o.Project(perspective);
        o *= scale;
        o += offset;

        PathGeometry path = new();

        PathFigureCollection figures = [];
        PathFigure figure = new() { IsClosed = true, StartPoint = new Windows.Foundation.Point(o.StartPoint.X, o.StartPoint.Y) };
        PathSegmentCollection segments = [];

        BezierSegment segment1 = new()
        {
            Point1 = new Windows.Foundation.Point(o.Segment1.Point1.X, o.Segment1.Point1.Y),
            Point2 = new Windows.Foundation.Point(o.Segment1.Point2.X, o.Segment1.Point2.Y),
            Point3 = new Windows.Foundation.Point(o.Segment1.Point3.X, o.Segment1.Point3.Y)
        };
        segments.Add(segment1);
        BezierSegment segment2 = new()
        {
            Point1 = new Windows.Foundation.Point(o.Segment2.Point1.X, o.Segment2.Point1.Y),
            Point2 = new Windows.Foundation.Point(o.Segment2.Point2.X, o.Segment2.Point2.Y),
            Point3 = new Windows.Foundation.Point(o.Segment2.Point3.X, o.Segment2.Point3.Y)
        };
        segments.Add(segment2);

        figure.Segments = segments;
        figures.Add(figure);
        path.Figures = figures;
        group.Children.Add(path);
    }

    public static void DrawCelestialBody(this Canvas canvas, CelestialBody body, Geometry.Projection perspective, Geometry.Vector offset, float scale = 1)
    {
        body.Render(perspective, offset, scale);
        canvas.Children.Add(body.OrbitPath);
    }
}
