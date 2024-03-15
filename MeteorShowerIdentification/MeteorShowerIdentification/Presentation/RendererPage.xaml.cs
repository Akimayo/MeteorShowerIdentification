using MeteorShowerIdentification.Business;
using MeteorShowerIdentification.Rendering;
using MeteorShowerIdentification.Rendering.Astrodynamics;

namespace MeteorShowerIdentification.Presentation;
public sealed partial class RendererPage : Page
{
    public RendererPage()
    {
        InitializeComponent();
        Renderer.Loaded += Renderer_Loaded;
    }

    private void Renderer_Loaded(object sender, RoutedEventArgs e)
    {
        Render(new(new(0, 0, 10)), 10);
        PerspX.ValueChanged += PerspectiveChanged;
        PerspY.ValueChanged += PerspectiveChanged;
        PerspZ.ValueChanged += PerspectiveChanged;
        Scale.ValueChanged += PerspectiveChanged;
    }

    private void PerspectiveChanged(object sender, Microsoft.UI.Xaml.Controls.Primitives.RangeBaseValueChangedEventArgs e)
    {
        Render(new(new((float)PerspX.Value, (float)PerspY.Value, (float)PerspZ.Value)), (float)Scale.Value);
    }

    private void Render(Rendering.Geometry.Projection perspective, float scale)
    {
        Rendering.Geometry.Vector offset = new((float)Renderer.ActualWidth / 2, (float)Renderer.ActualHeight / 2);
        Renderer.Children.Clear();
        foreach (CelestialBody c in StaticData.Planets) Renderer.DrawCelestialBody(c, perspective, offset, scale);
        //foreach (CelestialBody c in StaticData.OrthogonalOrbits) Renderer.DrawCelestialBody(c, perspective, offset, scale);
        foreach (CelestialBody c in StaticData.SimilarOrbits) Renderer.DrawCelestialBody(c, perspective, offset, scale);
        Renderer.DrawCelestialBody(StaticData.Sun, perspective, offset, scale);
    }
}
