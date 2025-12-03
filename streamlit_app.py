
import React, { useState, useEffect, useMemo } from 'react';
import { Purchase, CategoryType, ProductDef } from './types';
import { CATEGORIES, BADGES, ECO_TIPS, PRODUCTS } from './constants';
import { Dashboard } from './components/Dashboard';
import { PlusCircle, ShoppingBag, Trash2, Award, Info, Leaf, Search, Download, Sprout, Shirt, Feather, Shield, Ban, TrendingUp } from 'lucide-react';

// Icon mapper for dynamic badges
const BadgeIcon = ({ name, color, size = 16, className }: { name: string; color?: string; size?: number; className?: string }) => {
  const icons: Record<string, any> = {
    sprout: Sprout,
    shirt: Shirt,
    feather: Feather,
    shield: Shield,
    ban: Ban,
    'trending-up': TrendingUp
  };
  const Icon = icons[name] || Award;
  return <Icon size={size} className={className || color} />;
};

export default function App() {
  const [purchases, setPurchases] = useState<Purchase[]>(() => {
    const saved = localStorage.getItem('shopImpact_purchases');
    return saved ? JSON.parse(saved) : [];
  });

  const [form, setForm] = useState({
    productId: '',
    productName: '',
    brand: '',
    price: '',
    category: 'Cotton' as CategoryType
  });

  const [suggestion, setSuggestion] = useState<string | null>(null);

  // Group products for the dropdown
  const productGroups = useMemo(() => {
    const groups: Record<string, ProductDef[]> = {};
    PRODUCTS.forEach(p => {
      if (!groups[p.group]) groups[p.group] = [];
      groups[p.group].push(p);
    });
    return groups;
  }, []);

  // Get current product def if selected
  const selectedProduct = useMemo(() => {
    return PRODUCTS.find(p => p.id === form.productId);
  }, [form.productId]);

  useEffect(() => {
    localStorage.setItem('shopImpact_purchases', JSON.stringify(purchases));
  }, [purchases]);

  // Check for suggestion when category changes
  useEffect(() => {
    const catDef = CATEGORIES[form.category];
    if (catDef && catDef.suggestion && !catDef.isEco) {
      setSuggestion(catDef.suggestion);
    } else {
      setSuggestion(null);
    }
  }, [form.category]);

  const handleProductChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const pId = e.target.value;
    const prod = PRODUCTS.find(p => p.id === pId);
    
    if (prod) {
      setForm(prev => ({
        ...prev,
        productId: pId,
        productName: prod.label,
        category: prod.defaultCategory,
        brand: '' // Reset brand on product change so user picks from new list
      }));
    } else {
      setForm(prev => ({ ...prev, productId: '' }));
    }
  };

  const handleAddPurchase = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.productName || !form.price) return;

    const priceNum = parseFloat(form.price);
    const catDef = CATEGORIES[form.category];
    const impact = priceNum * catDef.multiplier;

    const newPurchase: Purchase = {
      id: Date.now().toString(),
      date: new Date().toISOString(),
      productName: form.productName,
      brand: form.brand,
      price: priceNum,
      category: form.category,
      co2Impact: impact
    };

    setPurchases([...purchases, newPurchase]);
    setForm({ productId: '', productName: '', brand: '', price: '', category: 'Cotton' });
    setSuggestion(null);
  };

  const handleDelete = (id: string) => {
    setPurchases(purchases.filter(p => p.id !== id));
  };

  const exportToCSV = () => {
    if (purchases.length === 0) return;

    const headers = ['ID', 'Date', 'Product Name', 'Brand', 'Price (INR)', 'Category', 'CO2 Impact (kg)'];
    const rows = purchases.map(p => [
      p.id,
      new Date(p.date).toLocaleDateString(),
      `"${p.productName.replace(/"/g, '""')}"`, // Escape quotes
      `"${p.brand.replace(/"/g, '""')}"`,
      p.price.toFixed(2),
      p.category,
      p.co2Impact.toFixed(3)
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(r => r.join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `shopimpact_data_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const activeBadges = BADGES.filter(b => b.condition(purchases));
  const randomTip = ECO_TIPS[Math.floor(Math.random() * ECO_TIPS.length)];

  // For the slider logic
  const currentPrice = form.price ? parseFloat(form.price) : 0;
  // Dynamic max for slider: if price > 10000, slider scales to fit, otherwise 10000 default
  const sliderMax = Math.max(10000, currentPrice);

  return (
    <div className="min-h-screen bg-stone-100 text-stone-800 font-sans selection:bg-emerald-200">
      
      {/* Header */}
      <header className="bg-stone-900 text-stone-50 py-6 sticky top-0 z-10 shadow-md">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="bg-emerald-500 p-2 rounded-lg text-white">
              <Leaf size={24} />
            </div>
            <h1 className="text-2xl font-serif font-bold tracking-wide">ShopImpact</h1>
          </div>
          <div className="text-xs sm:text-sm text-stone-400">
            Conscious Shopping Dashboard
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 sm:px-6 py-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Column: Form & History (4 cols) */}
        <div className="lg:col-span-4 space-y-6">
          
          {/* Add Purchase Form */}
          <section className="bg-white p-6 rounded-2xl shadow-sm border border-stone-200">
            <h2 className="text-xl font-bold font-serif mb-4 flex items-center gap-2 text-stone-800">
              <PlusCircle className="text-emerald-600" />
              New Purchase
            </h2>
            
            <form onSubmit={handleAddPurchase} className="space-y-4">
              <div>
                <label className="block text-xs font-bold uppercase text-stone-500 mb-1">Select Product</label>
                <div className="relative">
                  <select 
                    required
                    value={form.productId}
                    onChange={handleProductChange}
                    className="w-full rounded-lg border-stone-300 bg-stone-50 focus:border-emerald-500 focus:ring focus:ring-emerald-200 transition-all p-2.5 appearance-none"
                  >
                    <option value="">-- Choose an item --</option>
                    {Object.keys(productGroups).map(group => (
                      <optgroup key={group} label={group}>
                        {productGroups[group].map(p => (
                          <option key={p.id} value={p.id}>{p.label}</option>
                        ))}
                      </optgroup>
                    ))}
                  </select>
                  <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-stone-500">
                    <Search size={16} />
                  </div>
                </div>
              </div>

              <div>
                 <label className="block text-xs font-bold uppercase text-stone-500 mb-1">Price (₹)</label>
                 <div className="space-y-2">
                   {/* Slider Control */}
                   <div className="flex items-center gap-2">
                      <span className="text-xs text-stone-400">0</span>
                      <input 
                        type="range"
                        min="0"
                        max={sliderMax}
                        step="50"
                        value={currentPrice}
                        onChange={e => setForm({...form, price: e.target.value})}
                        className="w-full h-2 bg-stone-200 rounded-lg appearance-none cursor-pointer accent-emerald-600"
                      />
                      <span className="text-xs text-stone-400">{sliderMax > 10000 ? (sliderMax/1000).toFixed(0)+'k' : '10k'}</span>
                   </div>
                   
                   {/* Precise Input */}
                   <input 
                    type="number" 
                    required
                    min="0"
                    step="0.01"
                    value={form.price}
                    onChange={e => setForm({...form, price: e.target.value})}
                    className="w-full rounded-lg border-stone-300 bg-stone-50 focus:border-emerald-500 focus:ring focus:ring-emerald-200 transition-all p-2.5"
                    placeholder="0.00"
                  />
                 </div>
              </div>

              <div>
                   <label className="block text-xs font-bold uppercase text-stone-500 mb-1">Brand</label>
                   <input 
                    type="text" 
                    list="brand-list"
                    value={form.brand}
                    onChange={e => setForm({...form, brand: e.target.value})}
                    className="w-full rounded-lg border-stone-300 bg-stone-50 focus:border-emerald-500 focus:ring focus:ring-emerald-200 transition-all p-2.5"
                    placeholder={selectedProduct ? "Select or type..." : "Pick product first"}
                    disabled={!selectedProduct}
                  />
                  <datalist id="brand-list">
                    {selectedProduct && selectedProduct.brands.map(b => (
                      <option key={b} value={b} />
                    ))}
                  </datalist>
              </div>

              <div>
                <label className="block text-xs font-bold uppercase text-stone-500 mb-1">Material / Impact Category</label>
                <select 
                  value={form.category}
                  onChange={e => setForm({...form, category: e.target.value as CategoryType})}
                  className="w-full rounded-lg border-stone-300 bg-stone-50 focus:border-emerald-500 focus:ring focus:ring-emerald-200 transition-all p-2.5"
                >
                  {Object.values(CATEGORIES).map(cat => (
                    <option key={cat.id} value={cat.id}>
                      {cat.label} {cat.isEco ? '(Eco)' : ''}
                    </option>
                  ))}
                </select>
                <p className="text-[10px] text-stone-400 mt-1">
                  Auto-selected based on product. Change if your item uses different materials (e.g. Bamboo vs Cotton).
                </p>
              </div>

              {/* Real-time Eco Nudge */}
              {suggestion && (
                <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 text-sm text-amber-800 flex items-start gap-2 animate-pulse">
                  <Info className="shrink-0 mt-0.5" size={16} />
                  <span>{suggestion}</span>
                </div>
              )}

              <button 
                type="submit" 
                className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 px-4 rounded-xl shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2"
              >
                <PlusCircle size={20} />
                Add to Dashboard
              </button>
            </form>
          </section>

          {/* Recent List */}
          <section className="bg-white p-6 rounded-2xl shadow-sm border border-stone-200">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-bold font-serif flex items-center gap-2 text-stone-800">
                <ShoppingBag className="text-stone-400" size={20} />
                Recent Items
              </h2>
              {purchases.length > 0 && (
                <button 
                  onClick={exportToCSV}
                  className="text-xs flex items-center gap-1 text-emerald-600 hover:text-emerald-700 font-medium px-3 py-1.5 rounded-lg bg-emerald-50 hover:bg-emerald-100 transition-colors"
                  title="Export data to CSV"
                >
                  <Download size={14} />
                  Export CSV
                </button>
              )}
            </div>

            <div className="space-y-3 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
              {purchases.length === 0 ? (
                <p className="text-stone-400 text-sm italic">No items tracked yet.</p>
              ) : (
                [...purchases].reverse().map(p => (
                  <div key={p.id} className="group flex items-center justify-between p-3 rounded-xl bg-stone-50 border border-stone-100 hover:border-emerald-200 transition-colors">
                    <div>
                      <div className="font-semibold text-stone-800">{p.productName}</div>
                      <div className="text-xs text-stone-500">
                        {p.brand && <span className="font-medium text-stone-600">{p.brand} • </span>}
                        {CATEGORIES[p.category].label} • ₹{p.price}
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className={`text-xs font-bold ${CATEGORIES[p.category].isEco ? 'text-emerald-600' : 'text-amber-600'}`}>
                        {p.co2Impact.toFixed(1)} kg CO2
                      </div>
                      <button onClick={() => handleDelete(p.id)} className="text-stone-300 hover:text-red-500 transition-colors">
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </section>

        </div>

        {/* Right Column: Dashboard & Visualization (8 cols) */}
        <div className="lg:col-span-8 space-y-8">
          
          <Dashboard purchases={purchases} badges={activeBadges} />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            {/* Gamification / Badges */}
            <section className="bg-white p-6 rounded-2xl shadow-sm border border-stone-200">
              <h3 className="text-lg font-serif font-bold text-stone-800 mb-4 flex items-center gap-2">
                <Award className="text-amber-500" />
                Achievements
              </h3>
              <div className="grid grid-cols-2 gap-3">
                {BADGES.map(badge => {
                   const isUnlocked = activeBadges.find(b => b.id === badge.id);
                   return (
                     <div key={badge.id} className={`p-3 rounded-xl border ${isUnlocked ? 'bg-stone-50 border-emerald-200' : 'bg-stone-50 border-stone-100 opacity-50 grayscale'}`}>
                       <div className="flex items-center gap-2 mb-1">
                          <BadgeIcon name={badge.icon} className={isUnlocked ? badge.color : 'text-stone-300'} />
                          <span className={`text-sm font-bold ${isUnlocked ? 'text-stone-800' : 'text-stone-400'}`}>{badge.label}</span>
                       </div>
                       <p className="text-[10px] text-stone-500 leading-tight">{badge.description}</p>
                     </div>
                   );
                })}
              </div>
            </section>

            {/* Eco Tip Sidebar */}
            <section className="bg-sky-50 p-6 rounded-2xl shadow-sm border border-sky-100 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-4 opacity-10">
                <Leaf size={100} className="text-sky-800" />
              </div>
              <h3 className="text-lg font-serif font-bold text-sky-900 mb-2 relative z-10">Did You Know?</h3>
              <p className="text-sky-800 text-sm italic relative z-10 leading-relaxed">
                "{randomTip.text}"
              </p>
            </section>
          </div>

        </div>

      </main>
    </div>
  );
}
